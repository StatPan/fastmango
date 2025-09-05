# Quick Start

This guide will help you create and run your first FastMango project in just a few minutes.

## 1. Create a New Project

Once FastMango is installed, you can create a new project using the `fastmango new` command. This command sets up a new project directory with all the necessary files and a sensible default structure.

```bash
fastmango new myproject
```

This will create a `myproject` directory in your current location.

### Project Templates

FastMango supports project templates to help you get started faster. You can specify a template using the `--template` option. For example, to create a project with a basic API structure, you can use:

```bash
fastmango new myproject --template=basic
```

If you don't specify a template, the `basic` template will be used by default.

## 2. Explore the Project Structure

Navigate into your new project directory:

```bash
cd myproject
```

You'll find a single file, `main.py`, in your new project directory. This file contains the core of your application.

This structure is designed to be familiar to Django developers while being optimized for modern API development.

## 3. Run the Development Server

FastMango comes with a built-in development server that automatically reloads your application when you make changes to the code. To start the server, use the `fastmango run` command:

```bash
fastmango run
```

You should see output similar to this:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12347]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 4. Access Your API

Your new FastMango application is now running! You can access it in your browser at `http://127.0.0.1:8000`.

### Interactive API Documentation

FastMango automatically generates interactive API documentation for your project using Swagger UI. You can access it by navigating to `http://127.0.0.1:8000/docs` in your browser.

From this interface, you can explore your API endpoints, see their request and response formats, and even try them out live.

## Next Steps

You've successfully created and run your first FastMango project. Now you're ready to start building your application. A good next step is to read about how to create your first FastMango app in the [Your First Project](./first-project.md) guide.
