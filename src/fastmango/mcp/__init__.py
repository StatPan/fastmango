"""
FastMango MCP Integration

This module provides MCP (Model Context Protocol) integration for FastMango,
enabling developers to create AI tools with Django-like productivity.
"""

from .config import MCPConfig
from .decorators import mcp_tool
from .server import MCPServer

__all__ = ["MCPConfig", "mcp_tool", "MCPServer"]