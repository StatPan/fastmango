# FastMango GitHub Issues Template

## Epic Issues (Phases)

### Epic 1: Core Framework Foundation
```markdown
# Epic: Core Framework Foundation (Phase 1)

## Overview
Establish the foundational architecture for FastMango, implementing the core MangoApp class with unified web/AI/MCP integration.

## Goals
- Unified development experience for web + AI + MCP
- Django-style productivity with FastAPI performance
- Type-safe integration across all components

## Scope
- [ ] Core MangoApp architecture
- [ ] Basic CLI tools (fastmango new/run)
- [ ] LLM engine integration
- [ ] MCP server integration
- [ ] Database layer with SQLModel

## Success Criteria
- Can create and run a basic FastMango project
- Web endpoints, LLM calls, and MCP tools work together
- Developer experience matches design goals

## Timeline
2-3 months

## Related Issues
Links to specific implementation issues below

---
Labels: epic, phase-1, core
Milestone: Phase 1 - Foundation
```

### Epic 2: AI & MCP Enhancement
```markdown
# Epic: AI & MCP Enhancement (Phase 2)

## Overview
Advanced AI/MCP features including multi-provider support, advanced tooling, and enhanced developer experience.

## Goals
- Multiple LLM provider support (OpenAI, Anthropic, Ollama)
- Advanced MCP capabilities and tool composition
- Enhanced debugging and development tools

## Dependencies
- Phase 1 completion
- Community feedback integration

## Timeline
1-2 months

---
Labels: epic, phase-2, ai, mcp
Milestone: Phase 2 - Enhancement
```

## Core Implementation Issues

### Issue 1: MangoApp Core Architecture
```markdown
# Implement MangoApp Core Class

## Description
Create the central MangoApp class that unifies FastAPI, Pydantic AI, and FastMCP into a single development interface.

## Requirements
- Initialize FastAPI app internally
- Integrate LLM engine (Pydantic AI)
- Integrate MCP server (FastMCP)
- Unified configuration management
- Auto-discovery of components

## Technical Specs
```python
class MangoApp:
    def __init__(
        self,
        database_url: Optional[str] = None,
        llm_config: Optional[LLMConfig] = None,
        mcp_config: Optional[MCPConfig] = None,
    ):
        # Implementation details
        pass
        
    def get(self, path: str):
        # FastAPI route decorator
        pass
        
    def llm_endpoint(self, path: str):
        # LLM-integrated endpoint decorator
        pass
        
    def mcp_tool(self, name: Optional[str] = None):
        # MCP tool registration decorator
        pass
```

## Acceptance Criteria
- [x] MangoApp class instantiates successfully
- [x] FastAPI integration working
- [ ] Basic LLM integration functional
- [ ] Basic MCP integration functional
- [x] Configuration system working
- [ ] Unit tests passing

---
Labels: core, architecture, high-priority
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

### Issue 2: CLI Tool Development
```markdown
# Implement FastMango CLI Tools

## Description
Create Typer-based CLI tools for project management and development workflow.

## Requirements
- `fastmango new <project>` - Create new project
- `fastmango run` - Start development server
- `fastmango --help` - Show help with fmgo alias suggestion
- Jinja2-based project templates

## Technical Specs
- Use Typer for CLI framework
- Jinja2 templates for code generation
- Support multiple project templates
- Error handling and validation

## Project Templates
1. **basic** - Simple web API + MCP server
2. **ai-chat** - Chat application with LLM integration
3. **public-data** - Public API wrapper template

## Acceptance Criteria
- [x] `fastmango new` creates working project
- [x] `fastmango run` starts development server
- [x] Templates generate valid code
- [ ] Help system suggests fmgo alias
- [ ] Error handling for invalid inputs

---
Labels: cli, developer-experience, high-priority
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

### Issue 3: Database Integration
```markdown
# Implement Database Layer with SQLModel

## Description
Integrate SQLModel + SQLAlchemy for Django-style ORM patterns with async support.

## Requirements
- SQLModel models with Django-style managers
- Async database operations
- Alembic integration for migrations
- Connection pooling and management

## Technical Specs
```python
# Django-style model interface
class User(Model):
    email: str = Field(unique=True)
    username: str = Field(max_length=150)
    
    objects = Manager()  # Django-style manager

# Usage
users = await User.objects.filter(email__contains="@example.com")
```

## Database Support
- PostgreSQL (primary)
- SQLite (development)
- MySQL (future)

## Acceptance Criteria
- [x] SQLModel models work with Manager pattern
- [x] Async queries functional
- [ ] Migrations system integrated
- [x] Connection pooling working
- [ ] Multiple database support

---
Labels: database, orm, high-priority
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

### Issue 4: LLM Engine Implementation
```markdown
# Implement LLM Engine with Pydantic AI

## Description
Create unified LLM interface supporting multiple providers with type-safe integration.

## Requirements
- Pydantic AI integration
- Multiple provider support (OpenAI, Anthropic, Ollama)
- Context management and caching
- MCP tool integration

## Technical Specs
```python
class LLMEngine:
    async def generate(
        self, 
        prompt: str,
        provider: Optional[str] = None,
        context: Optional[dict] = None
    ):
        # Implementation with automatic MCP tool context
        pass
```

## Provider Support
1. **OpenAI** - GPT models
2. **Anthropic** - Claude models  
3. **Ollama** - Local models
4. **Extensible** - Plugin system for new providers

## Acceptance Criteria
- [ ] Pydantic AI integration working
- [ ] Multi-provider support functional
- [ ] Context and caching implemented
- [ ] MCP tools automatically available in context
- [ ] Type-safe inference working

---
Labels: llm, ai, pydantic-ai, high-priority
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

### Issue 5: MCP Server Integration
```markdown
# Implement MCP Server Integration with FastMCP

## Description
Integrate FastMCP for seamless MCP server functionality within MangoApp.

## Requirements
- FastMCP integration
- Tool registration and discovery
- Database access for MCP tools
- API endpoint integration

## Technical Specs
```python
@app.mcp_tool()
def search_database(model_name: str, filters: dict):
    # Auto-generated database access tools
    pass

@app.mcp_tool("custom-tool")
def custom_function(param: str) -> dict:
    # Custom MCP tools
    pass
```

## Features
- Automatic tool registration
- Database access patterns
- API integration (MCP tools can call internal APIs)
- Tool composition and chaining

## Acceptance Criteria
- [ ] FastMCP server runs within MangoApp
- [ ] Tool registration working
- [ ] Database access from tools functional
- [ ] API integration working
- [ ] Tool discovery and documentation

---
Labels: mcp, fastmcp, tools, high-priority
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

## Use Case Validation Issues

### Issue 6: 국회 공공데이터 MCP Implementation
```markdown
# Implement 국회 공공데이터 MCP Server

## Description
Create a real-world validation of FastMango framework by implementing Korean National Assembly public data MCP tools.

## Requirements
- 열린국회정보 API integration
- 공공데이터포털 API wrapper
- NABOSTATS API support
- Team Popong data integration

## MCP Tools to Implement
- `search_assembly_members()` - 국회의원 검색
- `get_bill_info()` - 의안 정보 조회
- `get_budget_data()` - 예산 데이터 조회
- `get_assembly_statistics()` - 국회 통계 조회

## Technical Requirements
- API key management
- Rate limiting and caching
- Error handling for public APIs
- Data validation and normalization

## Deployment
- Oracle Cloud free tier deployment
- Public MCP server hosting
- Documentation and examples

## Acceptance Criteria
- [ ] All public data APIs integrated
- [ ] MCP tools functional and tested
- [ ] Deployed to Oracle Cloud
- [ ] Public documentation available
- [ ] Community feedback collected

---
Labels: use-case, public-data, deployment, phase-4
Assignee: @statpan
Milestone: Phase 4 - First Use Case
```

## Documentation Issues

### Issue 7: Developer Documentation
```markdown
# Create Comprehensive Developer Documentation

## Description
Create documentation covering installation, usage, and development patterns for FastMango.

## Requirements
- Installation guide
- Quick start tutorial
- API reference
- Architecture documentation
- Contributing guidelines

## Structure
```
docs/
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── first-project.md
├── guides/
│   ├── web-apis.md
│   ├── llm-integration.md
│   ├── mcp-tools.md
│   └── deployment.md
├── reference/
│   ├── cli.md
│   ├── api.md
│   └── configuration.md
└── contributing/
    ├── setup.md
    ├── architecture.md
    └── guidelines.md
```

## Acceptance Criteria
- [ ] Complete installation instructions
- [ ] Working quick start tutorial
- [ ] Comprehensive API reference
- [ ] Architecture documentation
- [ ] Contributing guidelines

---
Labels: documentation, developer-experience
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

## Quality Assurance Issues

### Issue 8: Testing Infrastructure
```markdown
# Implement Comprehensive Testing Suite

## Description
Set up testing infrastructure covering unit tests, integration tests, and end-to-end validation.

## Requirements
- Unit tests for core components
- Integration tests for component interaction
- End-to-end tests for CLI and workflows
- Performance benchmarking
- CI/CD pipeline setup

## Testing Framework
- pytest for test execution
- pytest-asyncio for async testing
- httpx for API testing
- Coverage reporting

## Test Categories
1. **Unit Tests** - Individual component testing
2. **Integration Tests** - Component interaction testing
3. **E2E Tests** - Full workflow validation
4. **Performance Tests** - Benchmark key operations

## Acceptance Criteria
- [ ] >90% test coverage
- [ ] All components unit tested
- [ ] Integration tests passing
- [ ] E2E workflows validated
- [ ] CI/CD pipeline functional

---
Labels: testing, quality-assurance, ci-cd
Assignee: @statpan
Milestone: Phase 1 - Foundation
```

---

## Issue Labels System

### Priority Labels
- `high-priority` - Critical for milestone completion
- `medium-priority` - Important but not blocking
- `low-priority` - Nice to have, future consideration

### Component Labels
- `core` - Core framework functionality
- `cli` - Command line tools
- `database` - Database and ORM features
- `llm` - LLM and AI integration
- `mcp` - MCP server functionality
- `documentation` - Documentation and guides
- `testing` - Testing and quality assurance

### Phase Labels
- `phase-1` - Foundation phase issues
- `phase-2` - Enhancement phase issues
- `phase-3` - Production phase issues
- `phase-4` - Use case validation phase

### Type Labels
- `epic` - Large multi-issue initiatives
- `feature` - New functionality
- `bug` - Bug fixes
- `enhancement` - Improvements to existing features
- `documentation` - Documentation updates

## Milestone Structure

1. **Phase 1 - Foundation** (2-3 months)
2. **Phase 2 - Enhancement** (1-2 months)
3. **Phase 3 - Production** (1-2 months)
4. **Phase 4 - First Use Case** (1 month)

---

*This issue template provides a comprehensive structure for managing FastMango development through GitHub Issues and Projects.*