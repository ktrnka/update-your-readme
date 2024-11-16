# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Suggests README updates based on 1) the pull request description 2) the code changes in the PR 3) commit messages
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Option to skip README checks for testing purposes

Currently only available for developers of this repo:
- If you comment on a README PR, it will regenerate the README using your feedback
- If you merge/close a PR with an unmerged README PR, it will automatically close the stale README PR

## Usage

Prerequisites:

- GitHub repository
- Anthropic API key

To use this action in your GitHub workflow, add the following step to your `.github/workflows/your-workflow.yml` file, replacing the version as needed:

```yaml
- uses: ktrnka/update-your-readme@v0.3
  with:
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    readme-file: README.md
    anthropic-model: "claude-3-5-sonnet-20240620"  # Optional: Choose your preferred Claude model
```
See `.github/workflows/suggest_readme_updates.yml` for an example.

Make sure to set up the `ANTHROPIC_API_KEY` secret in your repository settings. Note: The Action will not work on PRs from forks because this secret isn't available on workflows for those PRs.

### Model Configuration

You can specify which Anthropic model to use through the `anthropic-model` input parameter. This allows you to balance between quality and cost:
- `claude-3-5-sonnet-20240620` (default) - Recommended for quality
- `claude-3-5-haiku-latest` - Faster and more cost-effective option. Note that the behavior may change if you use `latest` rather than a specific version

In your repo settings, under Actions > General > Workflow Permissions be sure to check "Allow GitHub Actions to create and approve pull requests" and allow read/write from Github Actions:
![Workflow Permissions](workflow_permissions.png)

### Skipping README Check

To skip the README check for testing purposes, include "NO README REVIEW" in the pull request body. This will cause the action to exit without performing any updates.

## Development

### Testing

This project uses pytest for testing. To run the tests, execute the following command:

```
pytest
```

### Code Formatting

We use Black for code formatting. To format your code, run:

```
black .
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Ensure your code follows the project's coding standards (use Black for formatting).
2. Update the README if necessary.

### License

[MIT License](https://opensource.org/licenses/MIT)

### GitHub Actions Integration

This project includes GitHub Actions workflows that enhance the README update process:

1. **Suggest README Updates**: Defined in `.github/workflows/suggest_readme_updates.yml`, this workflow:
   - Uses the `ktrnka/update-your-readme@actions-iteration-speed` action
   - Runs the README update process
   - Creates a new pull request with the suggested changes
   - Adds a comment to the original pull request with a link to the suggested changes

2. **Close Stale README PRs**: Defined in `.github/workflows/close_stale_prs.yml`, this workflow:
   - Triggers when a pull request is closed
   - Runs a shell script to identify and close any stale README update PRs associated with the closed PR

3. **README Feedback**: Defined in `.github/workflows/readme_feedback.yml`, this workflow:
   - Handles feedback on README updates

To use these features, ensure that your repository has the necessary secrets set up (`ANTHROPIC_API_KEY`).

### Debugging

The action supports a `debug` input, which can be set to "true" to enable additional debugging information. This can be helpful when troubleshooting issues with the action.


### Use Markdown for Formatting
Markdown is a lightweight markup language that makes it easy to format and style text. Use headers, lists, tables, and other elements to organize your README and make it visually appealing.

### Emphasize Readability and Clarity
- Break down large blocks of text into smaller sections or bullet points to improve readability.
- Write using clear and concise language to ensure that your README is easily understood by users of varying technical expertise. Avoid using jargon or overly technical language without proper explanation.
