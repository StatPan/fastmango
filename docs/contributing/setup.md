# Contributor Setup

This guide will walk you through the process of setting up the FastMango project for development.

## 1. Fork and Clone the Repository

First, you'll need to fork the [FastMango repository](https://github.com/statpan/fastmango) on GitHub. This will create a copy of the repository in your own GitHub account.

Next, clone your forked repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/fastmango.git
cd fastmango
```

## 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage the project's dependencies. This will keep your global Python installation clean and avoid version conflicts.

To create a virtual environment, run:

```bash
python -m venv venv
```

And to activate it:

```bash
# On Windows
.\venv\Scripts\activate

# On macOS and Linux
source venv/bin/activate
```

## 3. Install Dependencies

FastMango uses [Poetry](https://python-poetry.org/) to manage its dependencies. To install all the required dependencies, including the development dependencies, run:

```bash
pip install -e ".[dev]"
```

This will install all the packages listed in the `pyproject.toml` file in editable mode.

## 4. Run the Tests

> **Note**: The testing infrastructure is still under development.

Once the testing infrastructure is in place, you will be able to run the tests using the following command:

```bash
pytest
```

## 5. Code Style and Linting

FastMango uses [Black](https://github.com/psf/black) for code formatting and [Ruff](https://github.com/astral-sh/ruff) for linting. Before you submit a pull request, please make sure to run these tools to ensure that your code conforms to the project's code style.

To run the code formatter, use:

```bash
black .
```

To run the linter, use:

```bash
ruff .
```

You're now all set up to contribute to FastMango!
