# fastmango MCP Integration Strategy

This document outlines the recommended strategy for integrating the Model Context Protocol (MCP) into the fastmango framework. The analysis of FastMCP 2.0 and the Anthropic MCP Python SDK has concluded that **FastMCP 2.0 is the ideal choice for this integration.**

## 1. Core Integration Principle: Embrace and Extend

The integration strategy should be to **embrace FastMCP 2.0 as the core MCP engine** and **extend its capabilities to provide a seamless, Django-like experience**. We should not try to reinvent the wheel or create a competing implementation. Instead, we should leverage the excellent work done in FastMCP 2.0 and focus on making it feel like a natural part of the fastmango ecosystem.

## 2. Proposed Integration Architecture

### A. Dependency
- fastmango will have a direct dependency on `fastmcp`.

### B. Configuration (`settings.py`)
- fastmango's `settings.py` will have a dedicated `MCP` or `FASTMCP` configuration section.
- This section will map directly to FastMCP's own settings, allowing developers to configure the MCP server from a familiar location.

```python
# myproject/settings.py

# ... other fastmango settings

FASTMCP_SETTINGS = {
    "debug": DEBUG,
    "log_level": "INFO",
    "warn_on_duplicate_tools": True,
    # ... other FastMCP settings
}
```

### C. App-Based MCP Servers (`mcp.py`)
- To mirror Django's app-based structure, fastmango will introduce a convention of defining an app's MCP server in a file named `mcp.py` within the app's directory.
- This `mcp.py` file will contain an instance of a `FastMCP` server, with its tools, resources, and prompts.

```python
# myapp/mcp.py
from fastmango.mcp import FastMCP # fastmango will re-export FastMCP

app_mcp = FastMCP(name="My App MCP Server")

@app_mcp.tool
def my_app_tool(param: str) -> str:
    return f"Hello from {param}"
```

### D. Auto-Discovery and Mounting
- fastmango's core application will automatically discover the `mcp.py` files in all `INSTALLED_APPS`.
- It will then use FastMCP 2.0's `mcp.mount()` feature to mount each app's `app_mcp` server onto a main, project-level MCP server.
- The mount prefix for each app will be the app's name by default (e.g., `/myapp`).

### E. CLI Integration (`fastmango.py`)
- The `fastmango.py` CLI tool will be extended with commands for managing the MCP server.
- These commands will wrap the underlying `fastmcp` CLI, providing a unified interface.

```bash
# Start the fastmango web server and the MCP server together
fastmango runserver

# Or run the MCP server separately
fastmango runmcp

# Interact with the MCP server
fastmango mcp ... # (e.g., fastmango mcp list-tools)
```

## 3. Implementation Steps

1.  **Add `fastmcp` as a dependency** to fastmango's `pyproject.toml`.
2.  **Implement the settings integration**, allowing `FASTMCP_SETTINGS` in `settings.py` to configure the main MCP server.
3.  **Implement the auto-discovery mechanism** that iterates through `INSTALLED_APPS` and looks for `mcp.py` files.
4.  **Implement the auto-mounting logic** that uses `mcp.mount()` to compose the final MCP server.
5.  **Extend the `fastmango.py` CLI** with the `runmcp` and `mcp` subcommands.
6.  **Update the fastmango documentation** to include a section on MCP integration, explaining the `mcp.py` convention and how to define tools.

## 4. Benefits of this Approach

-   **Leverages Best-in-Class Tooling**: We get all the power and features of FastMCP 2.0 without having to build it ourselves.
-   **Familiar Developer Experience**: The `mcp.py`-in-an-app pattern is intuitive for Django developers.
-   **Modular and Scalable**: The app-based approach allows for building large, modular MCP applications.
-   **Clean Separation of Concerns**: The web server and the MCP server can be developed and run independently, but they share the same project structure and configuration.

By following this strategy, fastmango can offer a powerful, best-in-class MCP integration that feels like a natural extension of the Django development experience.
