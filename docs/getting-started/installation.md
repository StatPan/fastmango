# Installation

Welcome to FastMango! This guide will walk you through the process of installing the framework on your system.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.12+**: FastMango is built with the latest async features and requires a modern version of Python. You can check your Python version by running:
  ```bash
  python --version
  ```
- **pip**: The package installer for Python. pip is usually installed by default with Python. You can check if it's installed by running:
    ```bash
    pip --version
    ```
- **A virtual environment (recommended)**: It's highly recommended to use a virtual environment to manage your project's dependencies. This keeps your global Python installation clean and avoids version conflicts.

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

## Standard Installation

The easiest way to install FastMango is with `pip`:

```bash
pip install fastmango
```

This will download and install the latest stable version of FastMango from the Python Package Index (PyPI).

## Verifying the Installation

Once the installation is complete, you can verify that FastMango was installed correctly by checking its version:

```bash
fastmango --version
```

This should print the installed version of FastMango. You can also see the available commands by running:

```bash
fastmango --help
```

Congratulations, you have successfully installed FastMango! You are now ready to create your first project.
