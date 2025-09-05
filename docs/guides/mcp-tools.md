# Guide: Creating MCP Tools

> **Note**: This feature is currently under development and not yet available in the latest version of FastMango. The information on this page reflects the planned implementation.

FastMango aims to provide first-class support for the Multi-Agent Communication Protocol (MCP), a standard for communication between AI agents and tools. This guide will walk you through the planned features for creating and using MCP tools in your FastMango applications.

## What is MCP?

MCP is a specification that defines a standard way for AI agents to discover, call, and interact with tools. By building your tools to be MCP-compliant, you can make them available to a wide range of AI agents and systems.

You can learn more about MCP by reading the [official MCP specification](https://mcp.ai/).

## The `@app.mcp_tool()` Decorator

The primary way to create MCP tools in FastMango will be through the `@app.mcp_tool()` decorator. This decorator will automatically register your function as an MCP tool and make it available to the MCP server.

Here's an example of how you might use it:

```python
from pydantic import BaseModel

class WeatherRequest(BaseModel):
    city: str
    country: str

class WeatherResponse(BaseModel):
    temperature: float
    conditions: str

@app.mcp_tool(
    name="get_weather",
    description="Gets the current weather for a given city.",
)
def get_weather(request: WeatherRequest) -> WeatherResponse:
    """
    This function gets the weather for a given city.
    """
    # In a real application, you would call a weather API here.
    # For this example, we'll just return some dummy data.
    return WeatherResponse(
        temperature=25.0,
        conditions="sunny",
    )
```

In this example:

1.  We define two Pydantic schemas: `WeatherRequest` for the tool's input, and `WeatherResponse` for the output.
2.  We create a function `get_weather` that takes a `WeatherRequest` object as input and returns a `WeatherResponse` object.
3.  We use the `@app.mcp_tool()` decorator to register the function as an MCP tool. We provide a `name` and `description` for the tool, which will be used by AI agents to discover and understand what the tool does.

## The MCP Server

FastMango will include a built-in MCP server that will automatically expose all of your registered MCP tools. You will be able to enable the MCP server by providing an `MCPConfig` to your `MangoApp` instance:

```python
from fastmango import MangoApp, MCPConfig

mcp_config = MCPConfig(
    # Configuration options for the MCP server will go here.
)

app = MangoApp(
    mcp_config=mcp_config,
)
```

Once the MCP server is enabled, AI agents will be able to connect to your application and start using your tools.

## Automatic Tool Discovery

One of the key features of MCP is automatic tool discovery. When an AI agent connects to your FastMango application, it will be able to query the MCP server to get a list of all the available tools, along with their names, descriptions, and input/output schemas.

This makes it easy for AI agents to understand what your tools can do and how to use them, without any manual configuration.

## Next Steps

As the MCP integration features are developed, this guide will be updated with more detailed information and examples. In the meantime, you can learn more about MCP by reading the [official specification](https://mcp.ai/).
