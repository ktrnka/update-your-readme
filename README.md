# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Analyzes pull requests for changes
- Suggests README updates based on new dependencies and project structure
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Provides informative logging output about update actions
- Option to skip README checks for testing purposes
- Automatically closes stale README PRs

## Prerequisites

- GitHub repository
- GitHub API token
- Anthropic API key

## Installation

To use this action in your GitHub workflow, add the following step to your `.github/workflows/your-workflow.yml` file:

```yaml
- uses: ktrnka/update-your-readme@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    repository: ${{ github.repository }}
    pull-request-number: ${{ github.event.pull_request.number }}
    readme-file: README.md
```

Ensure you have set up the `ANTHROPIC_API_KEY` secret in your repository settings.

## Usage

### Setting Up GitHub Actions

1. Go to your repository settings.
2. Under "Actions > General," check "Allow GitHub Actions to create and approve pull requests."
3. Enable read/write permissions for GitHub Actions.

### Skipping README Check

To skip the README check for testing purposes, include "NO README REVIEW" in the pull request body.

## Project Structure

```
.
├── .github
│   └── workflows
│       ├── suggest_readme_updates.yml
│       └── close_stale_prs.yml
├── src
│   ├── core.py
│   ├── close_stale_prs.sh
│   ├── test_github.ipynb
│   └── test_popular_repos.ipynb
├── .gitignore
├── NOTES.md
├── Pipfile
├── Pipfile.lock
├── README.md
└── action.yml
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](https://opensource.org/licenses/MIT)

## GitHub Actions Workflows

### Suggest README Updates

Defined in `.github/workflows/suggest_readme_updates.yml`:
- Uses the `ktrnka/update-your-readme@use_marketplace_action` action
- Runs the README update process
- Creates a new pull request with suggested changes
- Adds a comment to the original pull request with a link to the suggested changes

### Close Stale README PRs

Defined in `.github/workflows/close_stale_prs.yml`:
- Triggers when a pull request is closed
- Runs a shell script to identify and close any stale README update PRs associated with the closed PR

## Closing Stale README PRs

The `close_stale_prs.sh` script in the `src` directory:
- Identifies open pull requests with the "automated pr" label
- Closes PRs whose branch names match the pattern related to the closed parent PR
- Adds a comment explaining why the PR was closed

This helps keep the repository clean by removing outdated README update suggestions.

Note: The GitHub Actions workflows respect the "NO README REVIEW" flag in pull request bodies, allowing for skipping README checks when needed.