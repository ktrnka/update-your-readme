# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Analyzes pull requests for changes
- Suggests README updates based on new dependencies and project structure
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Command-line functionality for easy integration

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

[Add license information here]

