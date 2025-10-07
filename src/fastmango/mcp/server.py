"""
MCP Server for FastMango
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastmcp import FastMCP

from .config import MCPConfig
from .decorators import get_registry


class MCPServer:
    """
    MCP Server implementation for FastMango.
    
    This class provides MCP server functionality with dashboard integration.
    """
    
    def __init__(self, app: FastAPI, config: Optional[MCPConfig] = None):
        """
        Initialize the MCP server.
        
        Args:
            app: The FastAPI application instance
            config: MCP configuration
        """
        self.app = app
        self.config = config or MCPConfig()
        self.mcp = FastMCP(name=self.config.name)
        self._setup_mcp_server()
        self._setup_dashboard_routes()
        self._setup_health_check()
        self._setup_swagger_integration()
        self._integrate_with_fastapi()
    
    def _setup_mcp_server(self) -> None:
        """
        Set up the MCP server with registered tools.
        """
        registry = get_registry()
        tools = registry.get_tools()
        
        for tool_name, tool_info in tools.items():
            # Register the tool with FastMCP
            self.mcp.tool(
                name=tool_name,
                description=tool_info["description"]
            )(tool_info["function"])
    
    def _setup_dashboard_routes(self) -> None:
        """
        Set up dashboard routes for MCP tools.
        """
        if not self.config.enable_dashboard:
            return
        
        @self.app.get(self.config.dashboard_url, response_class=HTMLResponse)
        async def mcp_dashboard():
            """
            MCP Dashboard endpoint.
            """
            registry = get_registry()
            tools = registry.get_tools()
            
            # Generate dashboard HTML
            dashboard_html = self._generate_dashboard_html(tools)
            return dashboard_html
        
        @self.app.get(f"{self.config.dashboard_url}/api/tools")
        async def mcp_tools_api():
            """
            API endpoint to get MCP tools information.
            """
            registry = get_registry()
            tools = registry.get_tools()
            
            # Convert tools to API format
            tools_api = {}
            for tool_name, tool_info in tools.items():
                tools_api[tool_name] = {
                    "name": tool_info["name"],
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"],
                    "return_type": tool_info["return_type"]
                }
            
            return JSONResponse(content=tools_api)
        
        @self.app.post(f"{self.config.dashboard_url}/api/tools/{{tool_name}}/execute")
        async def execute_mcp_tool(tool_name: str, request: Request):
            """
            API endpoint to execute an MCP tool.
            """
            registry = get_registry()
            tool = registry.get_tool(tool_name)
            
            if not tool:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"Tool '{tool_name}' not found"}
                )
            
            try:
                # Parse request body
                body = await request.json()
                args = body.get("args", {})
                
                # Execute the tool
                result = await tool["function"](**args)
                
                return JSONResponse(content={
                    "result": result,
                    "success": True
                })
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={
                        "error": str(e),
                        "success": False
                    }
                )
    
    def _setup_health_check(self) -> None:
        """
        Set up health check endpoint.
        """
        if not self.config.enable_health_check:
            return
        
        @self.app.get(self.config.health_check_url)
        async def health_check():
            """
            Health check endpoint.
            """
            registry = get_registry()
            tools = registry.get_tools()
            
            return JSONResponse(content={
                "status": "healthy",
                "mcp_server": {
                    "name": self.config.name,
                    "version": self.config.version,
                    "tools_count": len(tools),
                    "tools": list(tools.keys())
                }
            })
    
    def _setup_swagger_integration(self) -> None:
        """
        Set up Swagger/OpenAPI integration for MCP tools.
        """
        if not self.config.enable_swagger:
            return
        
        # Add MCP tools to the OpenAPI schema
        registry = get_registry()
        tools = registry.get_tools()
        
        for tool_name, tool_info in tools.items():
            # Create a path for each tool
            path = f"/mcp/tools/{tool_name}"
            
            # Add the path to the OpenAPI schema
            self.app.openapi_schema["paths"][path] = {
                "post": {
                    "summary": tool_info["description"],
                    "operationId": f"execute_{tool_name}",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": tool_info["parameters"],
                                    "required": [
                                        name for name, param in tool_info["parameters"].items()
                                        if "default" not in param
                                    ]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "result": {
                                                "type": "object"
                                            },
                                            "success": {
                                                "type": "boolean"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {
                                                "type": "string"
                                            },
                                            "success": {
                                                "type": "boolean"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            # Add the route to the FastAPI app
            @self.app.post(path)
            async def execute_mcp_tool_swagger(tool_name: str = tool_name, request: Request = None):
                """
                Execute an MCP tool (Swagger integration).
                """
                registry = get_registry()
                tool = registry.get_tool(tool_name)
                
                if not tool:
                    return JSONResponse(
                        status_code=404,
                        content={"error": f"Tool '{tool_name}' not found"}
                    )
                
                try:
                    # Parse request body
                    body = await request.json()
                    
                    # Execute the tool
                    result = await tool["function"](**body)
                    
                    return JSONResponse(content={
                        "result": result,
                        "success": True
                    })
                except Exception as e:
                    return JSONResponse(
                        status_code=500,
                        content={
                            "error": str(e),
                            "success": False
                        }
                    )
    
    def _integrate_with_fastapi(self) -> None:
        """
        Integrate the MCP server with FastAPI.
        """
        # Mount the MCP server to the FastAPI app
        mcp_app = self.mcp.http_app()
        self.app.mount("/mcp", mcp_app)
    
    def _integrate_with_fastapi(self) -> None:
        """
        Integrate the MCP server with FastAPI.
        """
        # Mount the MCP server to the FastAPI app
        mcp_app = self.mcp.http_app()
        self.app.mount("/mcp", mcp_app)
    
    def _generate_dashboard_html(self, tools: Dict[str, Dict[str, Any]]) -> str:
        """
        Generate HTML for the MCP dashboard.
        """
        tools_json = json.dumps({name: {
            "name": info["name"],
            "description": info["description"],
            "parameters": info["parameters"]
        } for name, info in tools.items()})
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>FastMango MCP Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/vue@3.2.31/dist/vue.global.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/axios@0.26.1/dist/axios.min.js"></script>
        </head>
        <body>
            <div id="app" class="container mt-4">
                <h1>FastMango MCP Dashboard</h1>
                <div class="row">
                    <div class="col-md-6">
                        <h2>Available Tools</h2>
                        <div class="list-group">
                            <div v-for="tool in tools" :key="tool.name" 
                                 class="list-group-item" 
                                 :class="{'active': selectedTool === tool.name}"
                                 @click="selectTool(tool.name)">
                                <h5>{{{{ tool.name }}}}</h5>
                                <p>{{{{ tool.description }}}}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h2>Tool Executor</h2>
                        <div v-if="selectedTool">
                            <h3>{{{{ selectedToolInfo.name }}}}</h3>
                            <p>{{{{ selectedToolInfo.description }}}}</p>
                            
                            <form @submit.prevent="executeTool">
                                <div v-for="(param, name) in selectedToolInfo.parameters" :key="name" class="mb-3">
                                    <label :for="name" class="form-label">{{{{ name }}}} ({{{{ param.type }}}})</label>
                                    <input v-if="param.type === 'string'" type="text" class="form-control" :id="name" v-model="toolArgs[name]">
                                    <input v-else-if="param.type === 'integer'" type="number" class="form-control" :id="name" v-model.number="toolArgs[name]">
                                    <input v-else-if="param.type === 'number'" type="number" step="0.01" class="form-control" :id="name" v-model.number="toolArgs[name]">
                                    <input v-else-if="param.type === 'boolean'" type="checkbox" class="form-check-input" :id="name" v-model="toolArgs[name]">
                                    <textarea v-else class="form-control" :id="name" v-model="toolArgs[name]"></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                    Execute
                                </button>
                            </form>
                            
                            <div v-if="result" class="mt-3">
                                <h4>Result:</h4>
                                <pre class="bg-light p-3">{{{{ JSON.stringify(result, null, 2) }}}}</pre>
                            </div>
                            
                            <div v-if="error" class="mt-3">
                                <h4>Error:</h4>
                                <div class="alert alert-danger">{{{{ error }}}}</div>
                            </div>
                        </div>
                        <div v-else class="alert alert-info">
                            Select a tool from the list to execute it.
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                const app = Vue.createApp({{
                    data() {{
                        return {{
                            tools: {tools_json},
                            selectedTool: null,
                            toolArgs: {{}},
                            result: null,
                            error: null,
                            loading: false
                        }};
                    }},
                    computed: {{
                        selectedToolInfo() {{
                            return this.selectedTool ? this.tools[this.selectedTool] : null;
                        }}
                    }},
                    methods: {{
                        selectTool(name) {{
                            this.selectedTool = name;
                            this.toolArgs = {{}};
                            this.result = null;
                            this.error = null;
                            
                            // Initialize default values
                            if (this.selectedToolInfo) {{
                                for (const [paramName, param] of Object.entries(this.selectedToolInfo.parameters)) {{
                                    if (param.default !== undefined) {{
                                        this.toolArgs[paramName] = param.default;
                                    }}
                                }}
                            }}
                        }},
                        async executeTool() {{
                            this.loading = true;
                            this.result = null;
                            this.error = null;
                            
                            try {{
                                const response = await axios.post(`/mcp-dashboard/api/tools/${{this.selectedTool}}/execute`, {{
                                    args: this.toolArgs
                                }});
                                
                                this.result = response.data;
                            }} catch (err) {{
                                this.error = err.response?.data?.error || err.message;
                            }} finally {{
                                this.loading = false;
                            }}
                        }}
                    }}
                }});
                app.mount('#app');
            </script>
        </body>
        </html>
        """