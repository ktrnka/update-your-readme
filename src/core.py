from github import Github, Auth, Repository, PullRequest
import os
import sys
from argparse import ArgumentParser
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

github_client = Github(auth=Auth.Token(os.environ["GITHUB_TOKEN"]))


def repo_contents_to_markdown(repo: Repository, sha: str = "HEAD") -> str:
    markdown = ""
    for content in repo.get_git_tree(sha, recursive=True).tree:
        markdown += f"{content.path}\n"
    return markdown


def pull_request_to_markdown(pr: PullRequest) -> str:
    text = f"""
# [{pr.title}]){pr.html_url}
{pr.body or 'No description provided.'}

"""
    for file in pr.get_files():
        patch = file.patch or "Can't render patch."
        text += f"""## {file.filename}\n{patch}\n\n"""

    return text


# model notes
# What we used before: claude-3-5-sonnet-20240620
# Fast, cheap: claude-3-haiku-20240307
model = ChatAnthropic(
    model="claude-3-haiku-20240307",
    # On prompt caching:
    # https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
    # https://api.python.langchain.com/en/latest/chat_models/langchain_anthropic.chat_models.ChatAnthropic.html
    # NOTE: This throws a UserWarning that seems spurious
    extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
)


class UpdateRecommendation(BaseModel):
    should_update: bool = Field(
        description="Whether the README should be updated or not"
    )
    reason: str = Field(description="Reason for the recommendation")
    updated_readme: Optional[str] = Field(
        description="Updated README content, required if should_update is True, otherwise optional",
        default=None,
    )


# Copied from https://www.hatica.io/blog/best-practices-for-github-readme/
readme_guidelines = """
# README Guidelines

Provide a Brief Overview of the Project
Include a brief but informative description of your project's purpose, functionality, and goals. This helps users quickly grasp the value of your project and determine if it's relevant to their needs.
Example: A user-friendly weather forecasting app that provides real-time data, daily forecasts, and weather alerts for locations worldwide.

Installation and Setup
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
Headers, Lists, Tables, and More

Markdown is a lightweight markup language that makes it easy to format and style text. Use headers, lists, tables, and other elements to organize your README and make it visually appealing.

## Emphasize Readability and Clarity
Break Down Large Blocks of Text

Large blocks of text can be intimidating and challenging to read. Break down large paragraphs into smaller sections or bullet points to improve readability.

Use Clear and Concise Language

Write using clear and concise language to ensure that your README is easily understood by users of varying technical expertise. Avoid using jargon or overly technical language without proper explanation.

"""


prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=[
                {
                    # According to the github issue comments, this cannot have any Langchain prompt variables in it but we can do Python string interpolation
                    # Source: https://github.com/langchain-ai/langchain/discussions/25610
                    "text": f"""
You'll review a pull request and determine if the README should be updated, then suggest appropriate changes.

{readme_guidelines}
""",
                    "type": "text",
                    # This triggers caching for this message AND all messages before it in the pipeline, also including any tool prompts
                    # Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        ),
        HumanMessage(
            content="""
# Existing README
{readme_content}

# PR Patch
{pr_patch}

# User Feedback
{feedback}

# Task
Based on the above information, please provide a structured output indicating:
A) should_update: Should the README be updated?
B) reason: Why?
C) updated_readme: The updated README content (if applicable)

If the README should be updated, take care to write teh updated_readme
"""
        ),
    ]
)

pipeline = prompt | model.with_structured_output(UpdateRecommendation)


def review_pull_request(
    repo: Repository, pr: PullRequest, tries_remaining=1, feedback: str = None
) -> UpdateRecommendation:
    try:
        result = pipeline.invoke(
            {
                "readme_content": repo.get_contents(
                    "README.md", ref=pr.base.sha
                ).decoded_content.decode(),
                "pr_patch": pull_request_to_markdown(pr),
                "readme_guidelines": readme_guidelines,
                "feedback": feedback,
            }
        )

        # Trigger a retry if the updated README is required but not provided
        if result.should_update and not result.updated_readme:
            raise ValueError(
                "Updated README content is required if should_update is True"
            )

        return result
    except (ValidationError, ValueError) as e:
        if tries_remaining > 0:
            print("Validation error, trying again")
            return review_pull_request(repo, pr, tries_remaining - 1)
        else:
            raise e


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--repository", "-r", type=str, help="Repository name")
    parser.add_argument("--readme", type=str, help="README file")
    parser.add_argument("--pr", type=int, help="Pull request number")
    parser.add_argument("--feedback", type=str, help="User feedback for LLM")

    args = parser.parse_args()

    repo = github_client.get_repo(args.repository)
    pr = repo.get_pull(args.pr)

    if pr.body and "NO README REVIEW" in pr.body:
        print("Skipping README check")
        sys.exit(0)

    result = review_pull_request(repo, pr, feedback=args.feedback)

    if result.should_update and result.updated_readme:
        print(f"Updating README with suggested changes: {result.reason}")
        with open(args.readme, "w") as f:
            f.write(result.updated_readme)
    else:
        print(f"No updates suggested: {result.reason}")
