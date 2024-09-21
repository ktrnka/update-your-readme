from github import Github
from github import Auth
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate


load_dotenv()

github_client = Github(auth=Auth.Token(os.environ['GITHUB_TOKEN']))

def repo_contents_to_markdown(repo):
    markdown = ""
    for content in repo.get_contents(""):
        markdown += f"{content.path}\n"
    return markdown

def pull_request_to_markdown(pr):
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
    reason: Optional[str]
    patch: Optional[str]


# Generate the LangChain Claude prompt
prompt = PromptTemplate.from_template("""
# README Content
{readme_content}

# File Tree
{file_tree}

# PR Patch
{pr_patch}

# Task
Based on the above information, please provide a structured output indicating:
A) Should the README be updated?
B) Why?
C) A patch of the update to make.
""")
pipeline = prompt | model.with_structured_output(UpdateRecommendation)

def review_pull_request(repo, pr_number) -> UpdateRecommendation:
    pr = repo.get_pull(pr_number)
    
    result = pipeline.invoke({
        "readme_content": repo.get_contents("README.md").decoded_content.decode(),
        "file_tree": repo_contents_to_markdown(repo),
        "pr_patch": pull_request_to_markdown(pr)
    })
    return result