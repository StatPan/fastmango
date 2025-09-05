# Contribution Guidelines

We welcome contributions from the community! Whether you're a developer, a designer, or just an enthusiastic user, there are many ways to contribute to the FastMango project.

## Code of Conduct

First and foremost, we ask that you read and adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md). We are committed to providing a friendly, safe, and welcoming environment for all, regardless of gender, sexual orientation, disability, ethnicity, religion, or similar personal characteristic.

## How to Contribute

There are many ways to contribute to FastMango:

-   **Reporting Bugs**: If you find a bug, please open an issue on our [GitHub issue tracker](https://github.com/statpan/fastmango/issues). Please include as much detail as possible, including the version of FastMango you're using, the steps to reproduce the bug, and any relevant error messages.
-   **Suggesting Enhancements**: If you have an idea for a new feature or an improvement to an existing one, please open an issue on our GitHub issue tracker. We'd love to hear your ideas!
-   **Writing Documentation**: We're always looking for help to improve our documentation. If you find something that's unclear or missing, please open a pull request with your proposed changes.
-   **Contributing Code**: If you'd like to contribute code to FastMango, please see the "Pull Request Process" section below.

## Pull Request Process

1.  **Fork and clone the repository**: See the [Contributor Setup](./setup.md) guide for instructions on how to do this.
2.  **Create a new branch**: Create a new branch for your changes:
    ```bash
    git checkout -b my-new-feature
    ```
3.  **Make your changes**: Make your changes to the code, and be sure to add tests to cover your changes.
4.  **Run the tests and linter**: Before you submit your pull request, please make sure to run the tests and the linter to ensure that your code is working correctly and conforms to the project's code style.
5.  **Submit a pull request**: Push your changes to your forked repository and open a pull request against the `main` branch of the FastMango repository.
6.  **Code review**: One of the project maintainers will review your pull request and provide feedback. Please be patient, as it may take some time to review your changes.
7.  **Merge**: Once your pull request has been approved, it will be merged into the `main` branch. Congratulations, you're now a FastMango contributor!

## Styleguides

### Git Commit Messages

-   Use the present tense ("Add feature" not "Added feature").
-   Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
-   Limit the first line to 72 characters or less.
-   Reference issues and pull requests liberally after the first line.

### Python Styleguide

FastMango follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide. We use [Black](https://github.com/psf/black) to automatically format our code, so you don't have to worry about a lot of the details.
