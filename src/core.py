from github import Github, Auth, Repository, PullRequest
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate


load_dotenv()

github_client = Github(auth=Auth.Token(os.environ['GITHUB_TOKEN']))

def repo_contents_to_markdown(repo: Repository) -> str:
    markdown = ""
    for content in repo.get_contents(""):
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



model = ChatAnthropic(model='claude-3-5-sonnet-20240620')

class UpdateRecommendation(BaseModel):
    should_update: bool
    reason: str
    updated_readme: str

# Copied from https://www.hatica.io/blog/best-practices-for-github-readme/
readme_guidelines = """
# README Guidelines

## Provide a Brief Overview of the Project
Include a brief but informative description of your project's purpose, functionality, and goals. This helps users quickly grasp the value of your project and determine if it's relevant to their needs.
Example: A user-friendly weather forecasting app that provides real-time data, daily forecasts, and weather alerts for locations worldwide.

## Installation and Setup
List Prerequisites and System Requirements

Clearly outline any prerequisites, such as software dependencies or system requirements, for your project. This helps users determine if they can use your project on their system and prepares them for the installation process.

Example:

```
## Prerequisites
- Node.js 14.x or higher
- Python 3.8 or higher
- Windows, macOS, or Linux operating system
```

Step-by-Step Instructions for Installation and Setup

Provide clear, step-by-step instructions for installing and setting up your project. This helps users get started quickly and minimizes potential issues.

Example:

## Installation
```
git clone https://github.com/username/WeatherForecastApp.git

cd WeatherForecastApp

npm install

npm start
```

## Explain How to Use the Software

Describe how users can interact with and use your project. This helps them understand the capabilities and limitations of your software.

Example:
```
## Usage

To use the WeatherForecastApp, follow these steps:

1. Enter your location in the search bar.
2. Select the desired date range for your forecast.
3. Click "Get Forecast" to view the weather data.
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

prompt = PromptTemplate.from_template("""
You'll review a pull request and determine if the README should be updated, then suggest appropriate changes.

{readme_guidelines}

# Existing README
{readme_content}

# File Tree
{file_tree}

# PR Patch
{pr_patch}

# Task
Based on the above information, please provide a structured output indicating:
A) Should the README be updated?
B) Why?
C) The updated README content (if applicable)
                                      """)
pipeline = prompt | model.with_structured_output(UpdateRecommendation)

def review_pull_request(repo: Repository, pr_number: int) -> UpdateRecommendation:
    pr = repo.get_pull(pr_number)

    result = pipeline.invoke({
        "readme_content": repo.get_contents("README.md").decoded_content.decode(),
        "file_tree": repo_contents_to_markdown(repo),
        "pr_patch": pull_request_to_markdown(pr),
        "readme_guidelines": readme_guidelines
    })
    return result