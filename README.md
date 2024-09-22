# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Analyzes pull requests for changes
- Suggests README updates based on new dependencies and project structure
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Command-line functionality for easy integration
- GitHub Actions integration for automated README updates
- Automatically closes stale README PRs

## Prerequisites

- Python 3.11 or higher
- GitHub API token
- Anthropic API key
- GitHub CLI (gh) installed and authenticated

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ktrnka/update-your-readme.git
   cd update-your-readme
   ```

2. Install dependencies:
   ```
   pip install pipenv
   pipenv install
   ```

3. Set up environment variables:
   - `GITHUB_TOKEN`: Your GitHub API token
   - `ANTHROPIC_API_KEY`: Your Anthropic API key

## Usage

Run the script with the following command:

```
pipenv run python src/core.py --repository <owner>/<repo> --pr <pr_number> --readme <path_to_readme>
```

Replace:
- `<owner>/<repo>` with the GitHub repository name
- `<pr_number>` with the pull request number you want to analyze
- `<path_to_readme>` with the path to your README file (e.g., README.md)

### Skipping README Check

To skip the README check for testing purposes, include "NO README REVIEW" in the pull request body.

## Project Structure

```
.
├── .github
│   └── workflows
│       ├── close_stale_prs.yml
│       ├── readme_feedback.yml
│       └── suggest_readme_updates.yml
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

## GitHub Actions Integration

This project includes GitHub Actions workflows that enhance the README update process:

1. **Suggest README Updates**: Defined in `.github/workflows/suggest_readme_updates.yml`, this workflow:
   - Runs on pull requests to the main branch
   - Checks out the repository, sets up Python, and installs dependencies
   - Runs the README update script
   - Creates a new pull request with suggested changes
   - Adds a comment to the original pull request with a link to the suggested changes

2. **Close Stale README PRs**: Defined in `.github/workflows/close_stale_prs.yml`, this workflow:
   - Triggers when a pull request is closed
   - Runs a shell script to identify and close any stale README update PRs associated with the closed PR

3. **README Feedback**: Defined in `.github/workflows/readme_feedback.yml`, this workflow:
   - Triggers on pull request review comments
   - Processes feedback and updates the README accordingly

### Closing Stale README PRs

The `close_stale_prs.sh` script in the `src` directory is used to automatically close stale README PRs. It:
- Identifies open pull requests with the "automated pr" label
- Closes PRs whose branch names match the pattern related to the closed parent PR
- Adds a comment explaining why the PR was closed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](https://opensource.org/licenses/MIT)