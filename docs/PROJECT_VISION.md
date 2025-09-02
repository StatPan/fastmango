# FastMango: Project Vision and Philosophy

## 1. Core Philosophy

**FastMango** is an **AI-first web framework** that combines FastAPI's modern performance, FastMCP's AI tooling capabilities, and Django's high productivity patterns into a unified development experience for building modern web applications with integrated LLM and MCP functionality.

Our goal is to help developers build fast, stable, and scalable applications that seamlessly integrate web APIs, LLM capabilities, and MCP tools by focusing solely on business logic without complex integration overhead.

## 2. Inspiration

* **Django**: Intuitive ORM, robust authentication system, automated Admin, and "batteries-included" philosophy
* **FastAPI**: Async performance, automatic validation and API documentation through type hints
* **FastMCP**: Seamless MCP server integration and AI tool development patterns
* **Pydantic AI**: Type-safe LLM integration with modern Python patterns

## 3. Guiding Principles

* **AI-First**: Native integration of LLM and MCP capabilities as first-class citizens
* **Unified Development**: Single framework for web APIs, AI tools, and MCP servers
* **Convention over Configuration**: Enable developers to start quickly with reasonable defaults
* **Type Safety**: Full Pydantic integration across web, AI, and MCP components
* **Pluggable Architecture**: Extensible design supporting various LLM providers and MCP tools

## 4. Development Philosophy

### Problem We're Solving
- **Simple APIs** → FastAPI is sufficient
- **Real-world services** → Need authentication, complex business logic, admin interfaces
- **Current gaps** → Django (synchronous, heavy), Django-Ninja (fake async), or building everything from scratch

### Our Approach
Provide Django's familiar patterns with FastAPI's true async performance:
- Django-style project structure and conventions
- True async/await support (not fake async)
- Modern Python type safety with Pydantic + SQLModel
- Built-in productivity features (admin, auth, migrations)

## 5. Target Use Cases

### Primary Use Cases
* **API-first applications**: Modern web services with frontend frameworks
* **Side projects**: Rapid prototyping with production-ready features
* **Microservices**: Lightweight, scalable service architecture
* **AI-powered applications**: Python's ML ecosystem + modern web performance

### Out of Scope (Initially)
* Server-side HTML template rendering
* Django Forms system (replaced with serialization layer)
* Django's synchronous patterns (async-first approach)

## 6. Success Metrics

### Developer Experience
- **Time to first API**: < 5 minutes from `fjango init` to running server
- **Learning curve**: Django developers productive within 1 hour
- **Boilerplate reduction**: 70% less setup code vs pure FastAPI

### Technical Performance
- **Cold start**: < 2 seconds development server startup
- **Memory usage**: < 50MB for basic application
- **Response time**: < 100ms average API response

### Community Adoption
- **GitHub stars**: > 1,000 by Phase 3 completion
- **Monthly downloads**: > 10,000 by Phase 4 completion
- **Enterprise adoption**: > 100 companies by 2026

## 7. Competitive Positioning

| Framework | Strengths | Weaknesses | fjango Advantage |
|-----------|-----------|------------|------------------|
| **Django** | Productivity, batteries-included | Sync-only, heavy for APIs | Async performance + familiar patterns |
| **FastAPI** | Performance, modern Python | Boilerplate for real apps | Django productivity + FastAPI speed |
| **Django-Ninja** | Django + FastAPI syntax | Fake async, Django limitations | True async + lighter weight |
| **Django REST Framework** | Mature ecosystem | Synchronous limitations | Modern async + better DX |

## 8. Technology Choices Rationale

### Core Stack
* **FastAPI**: Proven async performance, excellent type support
* **SQLModel**: Best of SQLAlchemy + Pydantic, type-safe ORM
* **Alembic**: Industry standard for database migrations
* **Pydantic**: Excellent data validation and serialization

### AI Integration
* **Pydantic AI**: Type-safe LLM integration, fits our type-first approach
* **No LangChain dependency**: Avoid complexity, focus on core use cases

## 9. Open Source Strategy

### Development Model
* **Open core**: Core framework completely open source
* **Commercial services**: Hosting platform (fjango Cloud) for sustainability
* **Community-driven**: Accept contributions, maintain clear architecture

### Monetization Philosophy
* Core tools remain free forever
* Value-added services (hosting, enterprise features) support development
* No feature gating or artificial limitations in open source version

---

*"The productivity of Django, the performance of FastAPI, the future of Python web development"*