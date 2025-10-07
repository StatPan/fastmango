"""
MCP Decorators for FastMango
"""

import inspect
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps
import json

from fastmcp import FastMCP


class MCPToolRegistry:
    """
    Registry for MCP tools.
    """
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
    
    def register(self, func: Callable, name: Optional[str] = None, **kwargs) -> None:
        """
        Register a function as an MCP tool.
        
        Args:
            func: The function to register
            name: Optional name for the tool (defaults to function name)
            **kwargs: Additional tool configuration
        """
        tool_name = name or func.__name__
        
        # Extract function signature for schema generation
        sig = inspect.signature(func)
        parameters = {}
        
        for param_name, param in sig.parameters.items():
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else "string"
            param_default = param.default if param.default != inspect.Parameter.empty else None
            required = param_default == inspect.Parameter.empty
            
            param_info = {
                "type": self._get_json_type(param_type),
                "description": f"Parameter: {param_name}",
            }
            
            if not required:
                param_info["default"] = param_default
            
            parameters[param_name] = param_info
        
        # Extract return type
        return_type = sig.return_annotation if sig.return_annotation != inspect.Signature.empty else "any"
        
        # Store tool information
        self._tools[tool_name] = {
            "function": func,
            "name": tool_name,
            "description": func.__doc__ or f"Tool: {tool_name}",
            "parameters": parameters,
            "return_type": self._get_json_type(return_type),
            **kwargs
        }
    
    def _get_json_type(self, annotation) -> str:
        """
        Convert Python type annotation to JSON schema type.
        """
        if annotation == int:
            return "integer"
        elif annotation == float:
            return "number"
        elif annotation == bool:
            return "boolean"
        elif annotation == str:
            return "string"
        elif hasattr(annotation, "__origin__"):
            if annotation.__origin__ == list:
                return "array"
            elif annotation.__origin__ == dict:
                return "object"
        return "any"
    
    def get_tools(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered tools.
        """
        return self._tools.copy()
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific tool by name.
        """
        return self._tools.get(name)
    
    def clear(self) -> None:
        """
        Clear all registered tools.
        """
        self._tools.clear()


# Global registry instance
_registry = MCPToolRegistry()


def mcp_tool(name: Optional[str] = None, **kwargs) -> Callable:
    """
    Decorator to register a function as an MCP tool.
    
    Args:
        name: Optional name for the tool (defaults to function name)
        **kwargs: Additional tool configuration
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        # Register the function
        _registry.register(func, name, **kwargs)
        
        # Return the original function
        return func
    
    return decorator


def get_registry() -> MCPToolRegistry:
    """
    Get the global MCP tool registry.
    """
    return _registry


def clear_registry() -> None:
    """
    Clear the global MCP tool registry.
    """
    _registry.clear()