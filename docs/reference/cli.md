# CLI Reference

The FastMango command-line interface (CLI) is a powerful tool for creating, managing, and running your projects.

## `fastmango new`

The `new` command creates a new FastMango project with a default directory structure and files.

### Usage

```bash
fastmango new <project_name>
```

### Arguments

-   **`PROJECT_NAME`** (required): The name of the project to create. A new directory with this name will be created in the current working directory.

### Example

```bash
fastmango new myproject
```

This will create a new project in a directory named `myproject`.

## `fastmango run`

The `run` command starts the development server for your FastMango project.

### Usage

```bash
fastmango run [OPTIONS]
```

### Options

-   **`--host <host>`**: The host to bind the server to. Defaults to `127.0.0.1`.
-   **`--port <port>`**: The port to bind the server to. Defaults to `8000`.
-   **`--reload` / `--no-reload`**: Enable or disable auto-reloading. Defaults to `True`.

### Example

```bash
fastmango run --port 8080
```

This will start the development server on port 8080.

## `fastmango version`

The `version` command displays the currently installed version of the FastMango framework.

### Usage

```bash
fastmango version
```

### Example

```bash
fastmango version
```

This will print the version of FastMango, for example: `FastMango version: 0.1.0`.
