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

# JavaScript: The Language of the Web

JavaScript is a high-level, dynamic, and interpreted programming language that has become an essential part of web development. It is one of the three core technologies of the World Wide Web, alongside HTML and CSS. JavaScript enables developers to create interactive and dynamic web pages, making it a crucial tool for building modern web applications.

## Key Features of JavaScript

- **Client-side scripting:** JavaScript runs on the client-side, meaning it executes within the user's web browser. This allows for real-time interactivity and updates without the need for page reloads.

- **Object-oriented programming:** JavaScript supports object-oriented programming concepts, allowing developers to create reusable and modular code using objects and classes.

- **Event-driven programming:** JavaScript heavily relies on event-driven programming, where code is executed in response to user actions or other events, such as button clicks or mouse movements.

- **Cross-platform compatibility:** JavaScript code can run on various platforms and devices, including web browsers, servers (using Node.js), and mobile applications (using frameworks like React Native).

## Popular JavaScript Frameworks and Libraries

JavaScript has a vast ecosystem of frameworks and libraries that enhance its capabilities and simplify web development. Some popular ones include:

- **React:** A library for building user interfaces, React allows developers to create reusable UI components and efficiently update the DOM.

- **Angular:** A comprehensive framework for building single-page applications, Angular provides a structured approach to web development with features like dependency injection and two-way data binding.

- **Vue.js:** A progressive framework for building user interfaces, Vue.js focuses on simplicity and performance, making it easy to integrate into existing projects.

- **Node.js:** A runtime environment that allows JavaScript to be executed on the server-side, enabling the development of full-stack JavaScript applications.

- **jQuery:** A fast and concise library that simplifies HTML document traversing, event handling, and animation, making it easier to work with the DOM.

## Getting Started with JavaScript

To start learning JavaScript, you can begin by exploring online resources and tutorials. Here are a few recommended resources:

- [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
- [FreeCodeCamp - JavaScript Algorithms and Data Structures](https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/)

With its versatility and extensive ecosystem, JavaScript has become an indispensable tool for web developers. Whether you're building interactive websites, single-page applications, or server-side applications, JavaScript provides the power and flexibility to bring your ideas to life on the web.
