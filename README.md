# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Analyzes pull requests for changes
- Suggests README updates based on new dependencies and project structure
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Command-line functionality for easy integration
- Provides informative logging output about update actions

## Prerequisites

- Python 3.11 or higher
- GitHub API token
- Anthropic API key

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

## Project Structure

```
.
├── .github
│   └── workflows
│       └── suggest_readme_updates.yml
├── src
│   └── core.py
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

This project includes a GitHub Actions workflow that automatically suggests README updates for pull requests. The workflow is defined in `.github/workflows/suggest_readme_updates.yml` and performs the following steps:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs the README update script with the specified README file
5. Creates a new pull request with the suggested changes
6. Adds a comment to the original pull request with a link to the suggested changes

To use this feature, ensure that your repository has the necessary secrets set up (`GITHUB_TOKEN` and `ANTHROPIC_API_KEY`).