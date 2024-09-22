# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Analyzes pull requests for changes
- Suggests README updates based on new dependencies and project structure
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Command-line functionality for easy integration
- Provides informative logging output about update actions
- Option to skip README checks for testing purposes
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

The script will now provide informative output about its actions, including whether it's updating the README and the reason for the update.

### Skipping README Check

To skip the README check for testing purposes, include "NO README REVIEW" in the pull request body. This will cause the script to exit without performing any updates.

## Project Structure

```
.
├── .github
│   └── workflows
│       ├── suggest_readme_updates.yml
│       └── close_stale_prs.yml
├── src
│   ├── core.py
│   └── close_stale_prs.sh
├── .gitignore
├── NOTES.md
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](https://opensource.org/licenses/MIT)

## GitHub Actions Integration

This project includes GitHub Actions workflows that enhance the README update process:

1. **Suggest README Updates**: Defined in `.github/workflows/suggest_readme_updates.yml`, this workflow:
   - Checks out the repository
   - Sets up Python
   - Installs dependencies
   - Runs the README update script with the specified README file
   - Creates a new pull request with the suggested changes
   - Adds a comment to the original pull request with a link to the suggested changes

2. **Close Stale README PRs**: Defined in `.github/workflows/close_stale_prs.yml`, this workflow:
   - Triggers when a pull request is closed
   - Runs a shell script to identify and close any stale README update PRs associated with the closed PR

To use these features, ensure that your repository has the necessary secrets set up (`GITHUB_TOKEN` and `ANTHROPIC_API_KEY`).

### Closing Stale README PRs

The `close_stale_prs.sh` script in the `src` directory is used to automatically close stale README PRs. It:
- Identifies open pull requests with the "automated pr" label
- Closes PRs whose branch names match the pattern related to the closed parent PR
- Adds a comment explaining why the PR was closed

This helps keep the repository clean by removing outdated README update suggestions.

Note: The GitHub Actions workflows respect the "NO README REVIEW" flag in pull request bodies, allowing for skipping README checks when needed.