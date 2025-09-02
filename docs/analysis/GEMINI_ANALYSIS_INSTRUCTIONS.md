# Gemini Analysis Instructions for MCP Frameworks

## Overview
This document provides detailed instructions for analyzing FastMCP 2.0 and Anthropic MCP Python SDK to inform fjango's MCP integration strategy.

## Analysis Scope

### Repositories to Analyze
1. **FastMCP 2.0**: `docs/analysis/fastmcp-2.0/`
   - Independent framework by Prefect team
   - Comprehensive MCP toolkit
   - Main source: `src/fastmcp/`

2. **Anthropic MCP Python SDK**: `docs/analysis/anthropic-mcp-sdk/`
   - Official Anthropic implementation
   - Includes FastMCP 1.0
   - Main source: `src/mcp/`

## Analysis Framework

Please analyze each framework according to these categories:

### 1. Architecture & Design Patterns

**For each framework, document:**

#### A. Project Structure
```
- How are modules organized?
- What's the main entry point?
- How are tools/resources/prompts structured?
- What's the relationship between server and client?
```

#### B. Core Abstractions
```
- Main classes and their responsibilities
- How is the MCP protocol implemented?
- What design patterns are used (decorators, managers, etc.)?
- How is async/sync handled?
```

#### C. Configuration & Setup
```
- How do users configure servers?
- What are the initialization patterns?
- How are dependencies managed?
- What's the development workflow?
```

### 2. Developer Experience Analysis

#### A. API Design
```
- How do developers define MCP tools?
- What's the decoration/registration pattern?
- How intuitive is the API?
- Code examples of typical usage
```

#### B. Type Safety & Validation
```
- How are schemas generated?
- What's the Pydantic integration like?
- How are types handled for tools/resources?
- Error handling patterns
```

#### C. Development Workflow
```
- CLI tools available
- Testing patterns
- Hot reload/development server
- Debugging capabilities
```

### 3. Features & Capabilities

#### A. Core MCP Features
```
- Tools implementation
- Resources and templates
- Prompts support
- Client capabilities
```

#### B. Advanced Features
```
- Authentication & security
- Middleware/plugins
- Server composition
- Transport protocols
- Integration capabilities
```

#### C. Production Features
```
- Deployment options
- Monitoring/logging
- Performance characteristics
- Scalability considerations
```

### 4. Django-like Integration Potential

#### A. Configuration Similarities
```
- Settings-based configuration?
- App/module structure?
- Auto-discovery patterns?
- URL routing equivalents?
```

#### B. Development Patterns
```
- Management commands?
- Migration-like features?
- Admin interface potential?
- Testing framework integration?
```

#### C. Extensibility
```
- Plugin architecture?
- Middleware system?
- Hook system?
- Customization points?
```

## Analysis Output Format

For each framework, create a structured analysis document:

### FastMCP 2.0 Analysis
```markdown
# FastMCP 2.0 Comprehensive Analysis

## Executive Summary
- 2-3 sentences on overall assessment
- Key strengths and weaknesses
- Fit for fjango integration

## Architecture Analysis
[Detailed findings for each category above]

## Code Examples
[Key patterns with code snippets]

## Django Integration Assessment
[Specific evaluation for fjango compatibility]

## Recommendations
[Specific recommendations for fjango]
```

### Anthropic MCP SDK Analysis
```markdown
# Anthropic MCP Python SDK Comprehensive Analysis

[Same structure as above]
```

## Specific Analysis Instructions

### 1. Read Key Files First
Start with these files to understand each framework:

**FastMCP 2.0:**
- `README.md` - Overview and examples
- `src/fastmcp/__init__.py` - Main exports
- `src/fastmcp/server/__init__.py` - Server implementation
- `examples/` - Usage patterns
- `pyproject.toml` - Dependencies and project structure

**Anthropic MCP SDK:**
- `README.md` - Official documentation
- `src/mcp/__init__.py` - Main exports  
- `src/mcp/server/` - Server implementation
- `examples/` - Official examples
- `pyproject.toml` - Dependencies

### 2. Focus Areas for fjango Integration

Pay special attention to:
- **Decorator patterns** for tools/resources (similar to Django views)
- **Configuration systems** (settings.py equivalent)
- **Auto-discovery mechanisms** (like Django apps)
- **CLI tooling** (manage.py equivalent)
- **Testing patterns** (Django test integration)
- **Production deployment** (WSGI/ASGI equivalents)

### 3. Comparison Points

Create direct comparisons on:
- **Boilerplate required** for basic server
- **Learning curve** for Django developers
- **Type safety** and validation approaches
- **Production readiness** features
- **Community and ecosystem** size
- **Integration complexity** with Django patterns

## Deliverables

Please provide:

1. **FastMCP 2.0 Analysis Document** (`FASTMCP_2_ANALYSIS.md`)
2. **Anthropic MCP SDK Analysis Document** (`ANTHROPIC_MCP_ANALYSIS.md`)
3. **Comparative Analysis** (`FRAMEWORK_COMPARISON.md`)
4. **fjango Integration Recommendations** (`FJANGO_MCP_STRATEGY.md`)

## Analysis Depth Guidelines

- **High Priority**: Architecture, API design, Django integration potential
- **Medium Priority**: Advanced features, production capabilities  
- **Low Priority**: Internal implementation details, edge cases

## Questions to Answer

After analysis, these should be answerable:

1. Which framework aligns better with fjango's Django-like philosophy?
2. Which provides better developer experience for Django developers?
3. Which has better long-term sustainability?
4. Which would require less adaptation work for fjango integration?
5. Is there potential for a hybrid approach using both?

## Timeline

Please complete analysis in this order:
1. FastMCP 2.0 (comprehensive)
2. Anthropic MCP SDK (comprehensive)
3. Direct comparison
4. fjango strategy recommendations

---

**Note**: This analysis will directly inform fjango's MCP integration strategy and architecture decisions. Focus on practical implications for Django-style web framework development.