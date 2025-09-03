# FastMCP 2.0 Pain Points Analysis for fastmango Integration

This document analyzes the potential pain points, limitations, and gaps a Django developer might experience when using FastMCP 2.0. The goal is to identify opportunities for fastmango to improve the developer experience.

## 1. Developer Experience (DX) Issues

### Pain Point: Manual App Registration and Boilerplate
- **Problem**: In FastMCP 2.0, creating a modular, app-based architecture (like the `smart_home` example) is a manual process. A developer must create the app's directory structure, define the `app_mcp` server, and then manually import and `mount` it in the main server file. This becomes tedious and error-prone as the number of apps grows.
- **Django Comparison**: Django developers are used to a simple `django-admin startapp` command and simply adding the app's name to `INSTALLED_APPS`. The framework handles the discovery and wiring automatically.
- **fastmango Solution**: fastmango can implement an auto-discovery mechanism. It would iterate through `INSTALLED_APPS`, find a conventional file (e.g., `mcp.py`), and automatically mount the `app_mcp` server found within. This eliminates the manual import and mounting boilerplate.

### Pain Point: Lack of Custom Management Commands
- **Problem**: The `fastmcp` CLI is powerful for running the server, but it doesn't provide a clear, built-in way for developers to add their own custom commands specific to their application (e.g., for data backfills, report generation, etc.).
- **Django Comparison**: Django's `manage.py` has a robust system for creating custom management commands (`python manage.py my_custom_command`), which is a vital feature for many projects.
- **fastmango Solution**: fastmango can create its own extensible CLI (`fastmango.py`) that wraps the `fastmcp` CLI. It would provide a mechanism for apps to register their own commands, which fastmango would then discover and make available.

## 2. Architecture Limitations

### Limitation: No Integrated Database/ORM Story
- **Problem**: FastMCP 2.0 is completely decoupled from the database layer. A developer needs to manage their own database connections, sessions, and ORM (e.g., SQLModel, SQLAlchemy). There is no built-in unit of work or request-scoped session management that integrates with the MCP tool lifecycle.
- **Django Comparison**: Django's ORM is one of its killer features. Models are easily accessible, and the database connection is managed automatically as part of the request-response cycle. Developers don't think about session management for simple queries.
- **fastmango Solution**: fastmango can provide a tight integration with an async ORM like SQLModel. It could manage the database engine lifecycle and provide a request-scoped session object via a dependency injection system, making it easy to use the database within MCP tools without manual setup.

## 3. Django Pattern Gaps

### Gap: No Middleware System
- **Problem**: FastMCP 2.0 does not have a concept of middleware that can process requests before they hit a tool or responses after they are generated. While one could potentially add ASGI middleware if running over HTTP, this is not a core, transport-agnostic feature of the framework.
- **Django Comparison**: Django has a simple, powerful middleware system that allows for cross-cutting concerns like authentication, logging, and request modification to be handled cleanly.
- **fastmango Solution**: fastmango could implement its own MCP middleware concept. It could define a middleware interface that allows developers to write classes with `process_request` and `process_response` methods that would be executed for every tool call, regardless of the transport used.

### Gap: Settings Management is a Convention, Not a Framework Feature
- **Problem**: While the `smart_home` example uses a `settings.py` file, this is a pattern that the developer chose to implement, not a feature provided by FastMCP 2.0 itself. The framework loads settings from environment variables, but it doesn't provide the centralized, object-based settings management that Django does.
- **Django Comparison**: Django's `settings.py` is the canonical, central source of truth for a project's configuration.
- **fastmango Solution**: As outlined in the integration strategy, fastmango will make this a core feature. It will have its own `settings.py` and will know how to pass the relevant MCP-related settings to the underlying FastMCP server instance.

## 4. fastmango Opportunity Areas

Based on the analysis, here are the key opportunities for fastmango to add value on top of FastMCP 2.0.

| Problem Area                  | Current FastMCP Workaround                                     | fastmango Solution                                                                                             | Implementation Effort |
| ----------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------- |
| **App Modularity**            | Manually import and `mount` each app's server in a central file. | Auto-discover and mount MCP servers from a conventional file (`mcp.py`) in `INSTALLED_APPS`.              | Medium                |
| **Database Integration**      | Manually manage database engine, sessions, and transactions.   | Provide a built-in, request-scoped database session via dependency injection. Manage engine lifecycle.      | High                  |
| **Custom CLI Commands**       | Write separate scripts outside the framework.                  | Provide an extensible `fastmango.py` CLI that can discover and run custom commands from installed apps.      | Medium                |
| **Middleware**                | Add ASGI middleware (HTTP only) or wrap every tool manually.   | Implement a transport-agnostic MCP middleware system for processing requests and responses.               | High                  |
| **Centralized Settings**      | Rely on environment variables or a hand-rolled settings module. | Use a canonical `settings.py` file as the single source of truth for both fastmango and MCP configuration. | Low                   |
