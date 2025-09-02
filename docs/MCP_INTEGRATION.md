# fjango MCP Integration

> **Build MCP (Model Context Protocol) tools with Django-like productivity**

fjango provides seamless integration with the Model Context Protocol, enabling developers to create AI tools with familiar Django patterns while leveraging FastAPI's async performance.

## 🎯 Vision: MCP Tools Made Simple

### The Problem with Current MCP Development
```python
# Current MCP development - Complex boilerplate
from mcp import Server
from mcp.server.models import Tool, TextContent
import asyncio

class WeatherServer:
    def __init__(self):
        self.server = Server("weather-server")
        
    async def list_tools(self) -> list[Tool]:
        return [
            Tool(
                name="get_weather",
                description="Get weather for a city", 
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
                    "required": ["city"]
                }
            )
        ]
    
    async def call_tool(self, name: str, args: dict):
        if name == "get_weather":
            city = args.get("city")
            # Implementation...
            return [TextContent(type="text", text=f"Weather in {city}: Sunny")]
```

### The fjango Way - Django-Like Simplicity
```python
# fjango MCP - Simple and powerful
from fjango.mcp import mcp_tool

@mcp_tool
async def get_weather(city: str) -> dict:
    """Get current weather for a city"""
    # Your business logic here
    weather_data = await weather_service.fetch(city)
    return {
        "city": city,
        "temperature": weather_data.temp,
        "condition": weather_data.condition,
        "humidity": weather_data.humidity
    }

@mcp_tool
async def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search our internal database"""
    results = await database.search(query, limit=limit)
    return [{"id": r.id, "title": r.title, "content": r.content} for r in results]

# That's it! Auto-generated MCP server with proper schemas
```

## 🏗️ Architecture Overview

### Core Components

```python
# fjango MCP Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   @mcp_tool     │───▶│  Schema Gen     │───▶│   MCP Server    │
│   Decorators    │    │  (Pydantic)     │    │   (JSON-RPC)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Django-style    │    │   Type Safety   │    │ Claude/ChatGPT  │
│ Configuration   │    │   Validation    │    │   Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Features

1. **Type-Safe Tool Definition**: Automatic schema generation from Python type hints
2. **Django-Style Configuration**: Familiar settings-based tool management
3. **Auto-Discovery Modes**: Choose between explicit registration or auto-detection
4. **Async Native**: Built on FastAPI's async foundation
5. **Production Ready**: Built-in error handling, logging, and monitoring

## 🔧 Configuration Modes

fjango supports two configuration philosophies to accommodate different development styles:

### Explicit Mode (Django Style - Default)
```python
# settings.py
MCP_DISCOVERY_MODE = "explicit"  # Default

MCP_TOOLS = [
    'myapp.tools.weather',
    'myapp.tools.database', 
    'myapp.tools.email',
]

# Optional: Environment-specific configuration
MCP_TOOLS_DEVELOPMENT = MCP_TOOLS + ['myapp.tools.debug']
MCP_TOOLS_PRODUCTION = [t for t in MCP_TOOLS if 'debug' not in t]
```

### Auto Mode (FastAPI Style)
```python
# settings.py  
MCP_DISCOVERY_MODE = "auto"

# Optional: Fine-grained control
MCP_AUTO_INCLUDE_PATTERNS = ['tools.*', 'mcp_handlers.*']
MCP_EXCLUDE = [
    'tools.debug',
    'tools.experimental.*'
]
```

## 📋 Tool Definition Patterns

### Basic Tool Definition
```python
from fjango.mcp import mcp_tool
from typing import List, Optional

@mcp_tool
async def get_weather(city: str, units: str = "metric") -> dict:
    """
    Get current weather information for a city.
    
    Args:
        city: Name of the city
        units: Temperature units (metric, imperial, kelvin)
    
    Returns:
        Weather data including temperature, condition, and forecast
    """
    weather_data = await weather_api.get_current(city, units)
    return {
        "city": city,
        "temperature": weather_data.temperature,
        "condition": weather_data.condition,
        "humidity": weather_data.humidity,
        "forecast": weather_data.forecast
    }
```

### Advanced Tool with Complex Types
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    relevance_score: float

class SearchFilters(BaseModel):
    category: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_score: float = Field(default=0.0, ge=0.0, le=1.0)

@mcp_tool
async def advanced_search(
    query: str, 
    filters: SearchFilters = SearchFilters(),
    limit: int = Field(default=10, ge=1, le=100)
) -> List[SearchResult]:
    """
    Advanced search with filters and pagination.
    """
    results = await search_engine.search(
        query=query,
        category=filters.category,
        date_range=(filters.date_from, filters.date_to),
        min_score=filters.min_score,
        limit=limit
    )
    
    return [
        SearchResult(
            id=r.id,
            title=r.title, 
            content=r.content,
            created_at=r.created_at,
            relevance_score=r.score
        ) for r in results
    ]
```

### Tool with Authentication and Permissions
```python
from fjango.mcp import mcp_tool, require_auth
from fjango.auth import User

@mcp_tool
@require_auth(permissions=['database.read'])
async def get_user_data(user_id: int, current_user: User) -> dict:
    """
    Get user data - requires authentication and permissions.
    """
    if not current_user.can_access_user(user_id):
        raise PermissionError("Access denied")
        
    user_data = await User.objects.get(id=user_id)
    return {
        "id": user_data.id,
        "email": user_data.email,
        "name": user_data.name,
        "created_at": user_data.created_at.isoformat()
    }
```

## 🚀 Development Workflow

### 1. Project Setup (Django-style)
```bash
# Initialize fjango project
fjango startproject my-ai-tools
cd my-ai-tools

# Create MCP apps (like Django's startapp)
fjango startmcp weather
fjango startmcp database  
fjango startmcp email

# Project structure (Django-like)
my-ai-tools/
├── my_ai_tools/
│   ├── settings.py          # MCP_APPS configuration
│   ├── mcp.py              # MCP server setup
│   └── __init__.py
├── weather/                # MCP app 1
│   ├── __init__.py
│   ├── tools.py            # @mcp_tool definitions
│   ├── models.py           # Optional data models
│   └── tests.py            # Tool tests
├── database/               # MCP app 2
│   ├── __init__.py
│   ├── tools.py
│   └── tests.py
├── email/                  # MCP app 3
│   ├── __init__.py
│   ├── tools.py
│   └── tests.py
├── manage.py               # Django-style management
└── requirements.txt
```

### 2. Development Server
```bash
# Start development server with hot reload
fjango dev

# Output:
🔥 Starting fjango MCP server...

🤖 MCP Server: mcp://localhost:8000
📊 Available Tools:
  • get_weather (tools.weather)
  • search_database (tools.database) 
  • send_email (tools.utilities)

🔄 Watching for changes...
✅ Ready for Claude/ChatGPT connection
```

### 3. Testing Tools
```bash
# Test individual tools
fjango mcp test get_weather --args='{"city": "San Francisco"}'
fjango mcp test search_database --args='{"query": "python"}'

# Test with Claude Desktop
fjango mcp connect-claude
```

### 4. Production Deployment
```bash
# Build for production
fjango build

# Deploy to various platforms
fjango deploy railway
fjango deploy fly
fjango deploy --custom-server
```

## 🔐 Security and Authentication

### Built-in Security Features
```python
# settings.py
MCP_SECURITY = {
    'require_auth': True,
    'allowed_origins': ['claude.ai', 'chatgpt.com'],
    'rate_limiting': {
        'enabled': True,
        'requests_per_minute': 100,
        'burst': 20
    },
    'api_keys': {
        'enabled': True,
        'header_name': 'X-MCP-API-Key'
    }
}
```

### Custom Authentication
```python
from fjango.mcp.auth import MCPAuthBackend

class CustomMCPAuth(MCPAuthBackend):
    async def authenticate(self, api_key: str) -> Optional[User]:
        # Custom authentication logic
        user = await User.objects.filter(api_key=api_key).first()
        if user and user.is_active:
            return user
        return None

# settings.py
MCP_AUTH_BACKEND = 'myapp.auth.CustomMCPAuth'
```

## 📊 Monitoring and Analytics

### Built-in Dashboard
```python
# Automatic metrics collection
@mcp_tool
async def monitored_tool(param: str) -> dict:
    """This tool automatically tracks:
    - Call frequency
    - Response times  
    - Error rates
    - User patterns
    """
    return {"result": "data"}
```

### Dashboard Access
```bash
# View analytics dashboard
fjango dashboard

# Export usage data
fjango mcp analytics --export=csv --period=month
```

## 🌟 Integration Examples

### Claude Desktop Integration
```json
{
  "mcpServers": {
    "my-ai-tools": {
      "command": "fjango", 
      "args": ["mcp", "serve"],
      "cwd": "/path/to/my-ai-tools"
    }
  }
}
```

### Custom Client Integration
```python
from fjango.mcp.client import MCPClient

async def use_tools():
    client = MCPClient("mcp://localhost:8000")
    
    # Call tools from Python
    weather = await client.call_tool("get_weather", {"city": "Tokyo"})
    results = await client.call_tool("search_database", {"query": "AI"})
    
    print(f"Weather: {weather}")
    print(f"Search results: {results}")
```

## 🎯 Roadmap Integration

### Phase 1: Foundation (Current)
- [x] MCP protocol integration
- [x] Basic tool decorator system  
- [x] Type-safe schema generation
- [ ] Django-style configuration modes

### Phase 2: Developer Experience
- [ ] CLI development tools
- [ ] Testing framework integration
- [ ] Hot reload for tool changes
- [ ] Auto-generated documentation

### Phase 3: Production Features  
- [ ] Authentication and authorization
- [ ] Rate limiting and monitoring
- [ ] Multi-tenant support
- [ ] Cloud deployment integration

### Phase 4: Ecosystem
- [ ] Tool marketplace integration
- [ ] Plugin system for extensions
- [ ] Advanced analytics dashboard
- [ ] Enterprise security features

## 💡 Why fjango for MCP?

### vs Raw MCP Development
```python
# Raw MCP: 50+ lines of boilerplate
class WeatherServer:
    # Complex server setup, protocol handling, etc.

# fjango: 5 lines, production ready
@mcp_tool
async def get_weather(city: str) -> dict:
    return await weather_api.get(city)
```

### vs Other Frameworks
- **Django familiarity**: Developers know the patterns already
- **Type safety**: Pydantic integration for bulletproof APIs
- **Async native**: Built for modern AI workloads
- **Production ready**: Authentication, monitoring, deployment included

## 🚀 Getting Started

```bash
# Install fjango
pip install fjango[mcp]

# Create your first MCP project
fjango init my-tools --template=mcp

# Add your first tool
echo '@mcp_tool
async def hello_world(name: str) -> str:
    return f"Hello, {name}!"' > tools/hello.py

# Start the server
fjango dev

# Connect with Claude Desktop or any MCP client!
```

---

*fjango MCP integration brings Django's productivity to AI tool development, making it simple to build, deploy, and scale intelligent applications.*