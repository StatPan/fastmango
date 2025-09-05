# API Reference

This document provides a reference for the core classes and functions in the FastMango Python library.

## `fastmango.MangoApp`

This is the main application class. It's a wrapper around `fastapi.FastAPI` that adds support for databases, LLMs, and MCP tools.

### `__init__`

```python
def __init__(
    self,
    database_url: str | None = None,
    llm_config: LLMConfig | None = None,
    mcp_config: MCPConfig | None = None,
    **kwargs,
):
```

Creates a new `MangoApp` instance.

**Arguments:**

-   **`database_url`**: The connection string for the database.
-   **`llm_config`**: Configuration for the LLM engine (not yet implemented).
-   **`mcp_config`**: Configuration for the MCP server (not yet implemented).
-   **`**kwargs`**: Additional arguments to be passed to the `fastapi.FastAPI` constructor.

### Decorators

The `MangoApp` class provides decorators for creating API endpoints:

-   `@app.get(path, **kwargs)`
-   `@app.post(path, **kwargs)`
-   `@app.put(path, **kwargs)`
-   `@app.delete(path, **kwargs)`
-   `@app.patch(path, **kwargs)`

These decorators work just like the ones in FastAPI.

### Other Methods

-   **`include_router(router, **kwargs)`**: Includes a `fastapi.APIRouter` in the application.

## `fastmango.models.Model`

This is the base class for all data models in a FastMango application. It's a subclass of `sqlmodel.SQLModel` that adds a Django-style `objects` manager.

### `objects`

A class attribute that provides access to a `Manager` instance for the model.

### `save()`

An asynchronous method that saves the current instance to the database.

### `delete()`

An asynchronous method that deletes the current instance from the database.

## `fastmango.models.Manager`

This class provides a Django-style interface for querying the database.

### `all()`

An asynchronous method that retrieves all objects from the database.

### `filter(**kwargs)`

An asynchronous method that filters objects based on keyword arguments (exact match).

### `get(**kwargs)`

An asynchronous method that retrieves a single object or `None` if not found.

### `get_or_404(**kwargs)`

An asynchronous method that retrieves a single object or raises an `HTTPException` with a 404 status code if not found.

### `create(**kwargs)`

An asynchronous method that creates and saves a new object.
