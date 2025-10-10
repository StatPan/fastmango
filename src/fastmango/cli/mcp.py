"""
MCP CLI commands for FastMango
"""

import json
import sys
from typing import Dict, Any, Optional

import typer
from fastapi import FastAPI
import uvicorn

from ..mcp import MCPConfig, MCPServer
from ..mcp.decorators import get_registry


app = typer.Typer(
    name="mcp",
    help="MCP (Model Context Protocol) commands for FastMango.",
    add_completion=False,
)


@app.command("serve")
def serve_mcp(
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
    config_path: Optional[str] = typer.Option(None, help="Path to MCP config file"),
):
    """
    Start the MCP server.
    """
    # Load configuration
    mcp_config = MCPConfig()
    if config_path:
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
                mcp_config = MCPConfig(**config_data)
        except Exception as e:
            typer.echo(f"Error loading config: {e}", err=True)
            raise typer.Exit(1)
    
    # Create FastAPI app
    fastapi_app = FastAPI(title="FastMango MCP Server")
    
    # Initialize MCP server
    mcp_server = MCPServer(fastapi_app, mcp_config)
    
    # Start the server
    typer.echo(f"Starting FastMango MCP server on {host}:{port}")
    typer.echo(f"Dashboard: http://{host}:{port}{mcp_config.dashboard_url}")
    typer.echo(f"Health check: http://{host}:{port}{mcp_config.health_check_url}")
    typer.echo(f"Swagger docs: http://{host}:{port}{mcp_config.swagger_url}")
    
    uvicorn.run(
        fastapi_app,
        host=host,
        port=port,
        reload=reload,
    )


@app.command("list-tools")
def list_tools():
    """
    List all registered MCP tools.
    """
    registry = get_registry()
    tools = registry.get_tools()
    
    if not tools:
        typer.echo("No MCP tools registered.")
        return
    
    typer.echo("Registered MCP tools:")
    for tool_name, tool_info in tools.items():
        typer.echo(f"  - {tool_name}: {tool_info['description']}")
        typer.echo(f"    Parameters: {', '.join(tool_info['parameters'].keys())}")
        typer.echo()


@app.command("test-tool")
def test_tool(
    tool_name: str,
    args: Optional[str] = typer.Option(None, help="JSON string of arguments"),
):
    """
    Test an MCP tool.
    """
    registry = get_registry()
    tool = registry.get_tool(tool_name)
    
    if not tool:
        typer.echo(f"Tool '{tool_name}' not found.", err=True)
        raise typer.Exit(1)
    
    # Parse arguments
    tool_args = {}
    if args:
        try:
            tool_args = json.loads(args)
        except json.JSONDecodeError as e:
            typer.echo(f"Error parsing arguments: {e}", err=True)
            raise typer.Exit(1)
    
    # Execute the tool
    try:
        import asyncio
        result = asyncio.run(tool["function"](**tool_args))
        typer.echo(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        typer.echo(f"Error executing tool: {e}", err=True)
        raise typer.Exit(1)


@app.command("generate-config")
def generate_config(
    output_path: str = typer.Option("mcp_config.json", help="Path to output config file"),
):
    """
    Generate a sample MCP configuration file.
    """
    config = MCPConfig()
    config_dict = config.dict()
    
    try:
        with open(output_path, "w") as f:
            json.dump(config_dict, f, indent=2)
        typer.echo(f"Generated MCP configuration at {output_path}")
    except Exception as e:
        typer.echo(f"Error generating config: {e}", err=True)
        raise typer.Exit(1)


@app.command("run")
def run_mcp(
    project_path: str = typer.Argument(".", help="Path to FastMango project"),
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
):
    """
    Run a FastMango project with MCP support.
    """
    import os
    import importlib.util
    
    # Change to project directory
    os.chdir(project_path)
    
    # Import the project's main module
    try:
        spec = importlib.util.spec_from_file_location("main", "main.py")
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        # Get the FastMango app
        if hasattr(main_module, "app"):
            mango_app = main_module.app
        else:
            typer.echo("Error: Could not find FastMango app in main.py", err=True)
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error loading project: {e}", err=True)
        raise typer.Exit(1)
    
    # Start the server
    typer.echo(f"Starting FastMango project with MCP support on {host}:{port}")
    
    uvicorn.run(
        mango_app.asgi,
        host=host,
        port=port,
        reload=reload,
    )