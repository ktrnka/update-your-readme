import json
import warnings
from github import Github, Auth, Repository, PullRequest
import os
from argparse import ArgumentParser
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional, Type

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, JsonSchemaFormat, CompletionsFinishReason, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError, ServiceResponseError

load_dotenv()


def pull_request_to_markdown(pr: PullRequest, excluded_diff_types={"ipynb"}) -> str:
    """
    Format key information from the pull request as markdown suitable for LLM input
    """

    # TODO: Ways to trim it down dynamically if it's too long. Maybe dynamically exclude certain filetypes
    text = f"""
## [{pr.title}]){pr.html_url}
{pr.body or 'No description provided.'}

### Commit Messages
"""
    for commit in pr.get_commits():
        text += f"- {commit.commit.message}\n"

    print()

    for file in pr.get_files():
        patch = "Can't render patch."
        if file.patch and file.filename.split(".")[-1] not in excluded_diff_types:
            patch = file.patch
        text += f"""### {file.filename}\n{patch}\n\n"""

    return text


def gha_escape(s: str) -> str:
    """
    Escape a string for use in GitHub Actions outputs.
    Reference: https://github.com/orgs/community/discussions/26736#discussioncomment-3253165
    """
    return s.replace("%", "%25").replace("\n", "%0A").replace("\r", "%0D")


def test_gha_escape():
    assert gha_escape("test") == "test"
    assert gha_escape("test\n") == "test%0A"
    assert gha_escape("test\r") == "test%0D"
    assert gha_escape("test%") == "test%25"
    assert gha_escape("test\n\r%") == "test%0A%0D%25"


class ReadmeRecommendation(BaseModel):
    """
    Structured output for the README review task
    """

    should_update: bool = Field(
        description="Whether the README should be updated or not"
    )
    reason: str = Field(description="Reason for the recommendation")
    updated_readme: Optional[str] = Field(
        description="Updated README content, required if should_update is true, otherwise optional",
    )

    @model_validator(mode="after")
    def post_validation_check(self) -> "ReadmeRecommendation":
        if self.should_update and self.updated_readme is None:
            raise ValueError("updated_readme must be provided if should_update is True")

        return self

    def to_github_actions_outputs(self):
        return f"""
should_update={self.should_update}
reason={gha_escape(self.reason)}
"""
    
def pydantic_model_to_azure_schema(pydantic_type: Type) -> JsonSchemaFormat:
    schema = pydantic_type.schema()
    schema["additionalProperties"] = False

    return JsonSchemaFormat(
        name=pydantic_type.__name__,
        schema=schema,
        description=pydantic_type.__doc__.strip(),
        strict=True,
    )

def test_output_validation():
    # importing here because it's a dev dependency
    import pytest

    # test that it works normally
    ReadmeRecommendation(should_update=True, reason="test", updated_readme="test")

    # test that it fails with missing fields
    with pytest.raises(ValidationError):
        ReadmeRecommendation(should_update=True)

    # test that it passes if should_update is False and the updated_readme is missing
    ReadmeRecommendation(should_update=False, reason="test")

    # test that it fails if should_update is True and the updated_readme is missing
    with pytest.raises(ValidationError):
        ReadmeRecommendation(should_update=True, reason="test")


# Adapted from https://www.hatica.io/blog/best-practices-for-github-readme/
readme_guidelines = """
# README Guidelines

## Provide a Brief Overview of the Project
Include a brief but informative description of your project's purpose, functionality, and goals. This helps users quickly grasp the value of your project and determine if it's relevant to their needs.
Example: A user-friendly weather forecasting app that provides real-time data, daily forecasts, and weather alerts for locations worldwide.

## Installation and Setup
List Prerequisites and System Requirements

Clearly outline any prerequisites, such as software dependencies, system requirements, or environment variables, for your project. This helps users determine if they can use your project on their system and prepares them for the installation process.

Example:

```
## Prerequisites
- Node.js 14.x or higher
- Python 3.8 or higher
- Environment variables: OPENAI_API_KEY, ...
```

Step-by-Step Instructions for Installation and Setup

Provide clear, step-by-step instructions for installing and setting up your project. This helps users get started quickly and minimizes potential issues.

Example:

```
## Installation
git clone https://github.com/username/WeatherForecastApp.git

cd WeatherForecastApp

npm install

npm start
```

## Use Markdown for Formatting
Markdown is a lightweight markup language that makes it easy to format and style text. Use headers, lists, tables, and other elements to organize your README and make it visually appealing.

## Emphasize Readability and Clarity

* Large blocks of text can be challenging to read. Break down large paragraphs into smaller sections or bullet points to improve readability.
* Write using clear and concise language to ensure that your README is easily understood by users of varying technical expertise. Avoid using jargon or overly technical language without proper explanation.

## Avoid Ephemeral References
* Do not include references such as "recent changes," "recently improved," or similar time-based language. The README should be timeless, describing the current state of the project without assuming how new or old a feature is.

"""


def fill_prompt(
    readme: str, pull_request_markdown: str, feedback: str
) -> tuple[SystemMessage, UserMessage]:
    return SystemMessage(
                content=f"""
You'll review a pull request and determine if the README should be updated, then suggest appropriate changes.
The README should be updated if it contains outdated information or if the pull request introduces major new features that are similar to those currently documented in the README.

When updating the README, be sure to:
* Keep the language timeless. Do not reference "recent" or "recently."
* Focus on the current state of the project features and requirements.

{readme_guidelines}

"""), UserMessage(
                content=f"""
# Existing README
{readme}

# Pull request changes
{pull_request_markdown}

# Optional User Feedback about README updates
{feedback}

# Task
Based on the above information, please provide a structured output indicating:
A) should_update: Should the README be updated?
B) reason: Why?
C) updated_readme: The updated README content (if applicable)
"""
)

def test_fill_prompt():
    # Basic no-crash test
    assert "DEFAULT README" in fill_prompt("# DEFAULT README", "# PR STUFF", "")

def get_client() -> ChatCompletionsClient:
    return ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
        # Needed for structured output
        api_version="2024-12-01-preview",
    )

def get_readme(repo: Repository, pr: PullRequest, use_base_readme=False) -> str:
    return repo.get_contents(
            "README.md", ref=pr.base.sha if use_base_readme else pr.head.sha
        ).decoded_content.decode()

class UnsupportedModelError(ValueError):
    """
    Exception raised for errors in the model selection.

    Attributes:
        model -- the model that caused the error
        message -- explanation of the error
    """
    def __init__(self, model, message="Selected model is not supported"):
        self.model = model
        self.message = message
        super().__init__(self.message)

class LlmError(ValueError):
    pass

def review_pull_request(
    client: ChatCompletionsClient,
    model_name: str,
    repo: Repository,
    pr: PullRequest,
    tries_remaining=1,
    feedback: str = None,
    use_base_readme=False,
) -> ReadmeRecommendation:
    try:
        readme = get_readme(repo, pr, use_base_readme)
        pr_content = pull_request_to_markdown(pr)

        response = client.complete(
            messages=fill_prompt(readme, pr_content, feedback),
            model=model_name,
            temperature=0.2,
            # The max on my tier
            max_tokens=4000,
            top_p=0.1,
            response_format=pydantic_model_to_azure_schema(ReadmeRecommendation)
        )

        # Check the completion reason
        if response.choices[0].finish_reason != CompletionsFinishReason.STOPPED:
            raise LlmError(
                f"Completion did not finish, finish_reason={response.choices[0].finish_reason}, usage={response.usage}"
            )

        json_response_message = json.loads(response.choices[0].message.content)
        result = ReadmeRecommendation(**json_response_message)

        return result
    except (HttpResponseError, ServiceResponseError) as e:
        # Not a retryable error
        raise UnsupportedModelError(model_name) from e
    # Note: Handle retry-able errors differently from non-retryable errors
    except ValidationError as e:
        if tries_remaining > 1:
            # BUG? If this happens, and we're piping stdout to a file to parse the output it may break Github's output parsing
            # print("Validation error, trying again")
            return review_pull_request(repo, pr, tries_remaining - 1)
        else:
            raise e


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--repository", "-r", type=str, required=True, help="Repository name"
    )
    parser.add_argument("--readme", type=str, required=True, help="README file")
    parser.add_argument("--pr", type=int, required=True, help="Pull request number")
    parser.add_argument("--feedback", type=str, help="User feedback for LLM")

    parser.add_argument(
        "--model-provider",
        type=str,
        choices=["anthropic", "openai"],
        default="anthropic",
        help="LLM provider to use",
    )
    parser.add_argument(
        "--model", type=str, default="claude-3-5-sonnet-20240620", help="<odel to use"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="json",
        choices=["json", "github"],
        help="Output format",
    )

    args = parser.parse_args()

    github_client = Github(auth=Auth.Token(os.environ["GITHUB_TOKEN"]))
    repo = github_client.get_repo(args.repository)
    pr = repo.get_pull(args.pr)

    if pr.body and "NO README REVIEW" in pr.body:
        # Setup the result so the output is consistent
        result = ReadmeRecommendation(
            should_update=False, reason="'NO README REVIEW' in PR body"
        )
    else:
        model = get_client(args.model_provider, args.model)
        result = review_pull_request(model, repo, pr, feedback=args.feedback)

        if result.should_update and result.updated_readme:
            with open(args.readme, "w") as f:
                f.write(result.updated_readme)

    if args.output_format == "github":
        # If running in Github Actions, this output formatting will set action outputs and be printed
        print(result.to_github_actions_outputs())
    else:
        print(result.model_dump_json())
