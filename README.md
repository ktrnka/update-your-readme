# Update Your README

This project automatically updates README files based on changes in pull requests using GitHub API and language models.

## Features

- Suggests README updates based on 1) the pull request description 2) the code changes in the PR
- Uses LangChain and Anthropic's Claude model for intelligent suggestions
- Option to skip README checks for testing purposes
- Provides feedback on README updates through comments
- Automatically closes stale README PRs

## Usage

Prerequisites:

- GitHub repository
- Anthropic API key

To use this action in your GitHub workflow, add the following step to your `.github/workflows/your-workflow.yml` file, replacing the version as needed:

```yaml
- uses: ktrnka/update-your-readme@v1
  with:
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    readme-file: README.md
    debug: "false"
```
See `.github/workflows/suggest_readme_updates.yml` for an example.

Make sure to set up the `ANTHROPIC_API_KEY` secret in your repository settings. Note: The Action will not work on PRs from forks because this secret isn't available on workflows for those PRs.

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
   - Handles feedback on README updates by regenerating the README based on comments

To use these features, ensure that your repository has the necessary secrets set up (`ANTHROPIC_API_KEY`).

### Debugging

The action supports a `debug` input, which can be set to "true" to enable additional debugging information. This can be helpful when troubleshooting issues with the action.

### Error Handling

The workflows now include `continue-on-error: true` to prevent the entire workflow from failing if one step encounters an error. This improves the robustness of the automation process.

### Action Inputs

The main action (`action.yml`) now supports the following inputs:
- `anthropic-api-key`: Required. The API key for Anthropic's language model.
- `readme-file`: Required. The path to the README file to update (default: 'README.md').
- `debug`: Optional. Enable debug mode for additional logging (default: 'false').

Note: The `github-token`, `repository`, and `pull-request-number` inputs have been removed as they are now automatically obtained from the GitHub context.

## Output

The action now supports two output formats:
1. JSON: The default output format.
2. GitHub Actions: A format compatible with GitHub Actions outputs, which can be used to set action outputs and create comments.

You can specify the output format using the `--output-format` parameter in the `core.py` script.