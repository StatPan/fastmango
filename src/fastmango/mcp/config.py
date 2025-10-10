"""
MCP Configuration for FastMango
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class MCPConfig(BaseModel):
    """
    Configuration for MCP (Model Context Protocol) server.
    """
    
    # Server configuration
    name: str = Field(default="FastMango MCP Server", description="Server name")
    version: str = Field(default="1.0.0", description="Server version")
    
    # Discovery mode: "explicit" or "auto"
    discovery_mode: str = Field(default="explicit", description="Tool discovery mode")
    
    # Explicit mode configuration
    tools: List[str] = Field(default_factory=list, description="List of tool modules to include")
    
    # Auto mode configuration
    auto_include_patterns: List[str] = Field(
        default_factory=lambda: ["tools.*", "mcp_handlers.*"], 
        description="Patterns for auto-discovery"
    )
    exclude: List[str] = Field(default_factory=list, description="Modules to exclude")
    
    # Security configuration
    require_auth: bool = Field(default=False, description="Require authentication")
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["claude.ai", "chatgpt.com"], 
        description="Allowed origins for CORS"
    )
    
    # Rate limiting
    rate_limiting: Dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "requests_per_minute": 100,
            "burst": 20
        },
        description="Rate limiting configuration"
    )
    
    # API keys
    api_keys: Dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "header_name": "X-MCP-API-Key"
        },
        description="API key configuration"
    )
    
    # Dashboard integration
    enable_dashboard: bool = Field(default=True, description="Enable dashboard integration")
    dashboard_url: str = Field(default="/mcp-dashboard", description="Dashboard URL path")
    
    # Health check
    enable_health_check: bool = Field(default=True, description="Enable health check endpoint")
    health_check_url: str = Field(default="/health", description="Health check URL path")
    
    # Swagger/OpenAPI integration
    enable_swagger: bool = Field(default=True, description="Enable Swagger/OpenAPI integration")
    swagger_url: str = Field(default="/docs", description="Swagger UI URL path")