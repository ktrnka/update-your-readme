# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Analyzes pull requests for changes
- Suggests README updates based on new dependencies and project structure
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Command-line functionality for easy integration
- GitHub Actions integration for automated README update suggestions

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
pipenv run python src/core.py --repository &lt;owner&gt;/&lt;repo&gt; --pr &lt;pr_number&gt;
```

Replace `&lt;owner&gt;/&lt;repo&gt;` with the GitHub repository name and `&lt;pr_number&gt;` with the pull request number you want to analyze.

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
4. Runs the README update script
5. Creates a new pull request with the suggested changes
6. Adds a comment to the original pull request with a link to the suggested changes

Key features of the GitHub Actions workflow:

- Automatic triggering on pull request events
- Creates a new branch for suggested README changes
- Generates a descriptive title and body for the new pull request
- Adds labels to the new pull request for easy identification
- Comments on the original pull request with a link to the suggested changes

To use this feature, ensure that your repository has the necessary secrets set up (`GITHUB_TOKEN` and `ANTHROPIC_API_KEY`).

## Troubleshooting

If you encounter any issues while using this project, please check the following:

1. Ensure all prerequisites are installed and up to date
2. Verify that your environment variables are correctly set
3. Check the GitHub Actions logs for any error messages

If problems persist, please open an issue on the GitHub repository with a detailed description of the problem and steps to reproduce it.
