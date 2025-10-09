from fastapi import FastAPI, Request
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import db_session_context
from .mcp import MCPConfig, MCPServer

# This is a placeholder for future implementation.
class LLMConfig:
    pass

class MangoApp:
    """
    The main application class for FastMango. This class unifies FastAPI,
    database, LLM, and MCP functionalities into a single interface.
    """
    def __init__(
        self,
        database_url: Optional[str] = None,
        llm_config: Optional[LLMConfig] = None,
        mcp_config: Optional[MCPConfig] = None,
        enable_admin: bool = True,
        admin_url: str = "/admin",
        **kwargs,
    ):
        """
        Initializes the MangoApp.

        Args:
            database_url: The connection string for the database.
            llm_config: Configuration for the LLM engine.
            mcp_config: Configuration for the MCP server.
            enable_admin: Whether to enable the admin interface (default: True).
            admin_url: URL path for the admin interface (default: "/admin").
            **kwargs: Additional arguments to be passed to the FastAPI constructor.
        """
        self.fastapi_app = FastAPI(**kwargs)
        self.db_url = database_url
        self.llm_config = llm_config
        self.mcp_config = mcp_config
        self.enable_admin = enable_admin
        self.admin_url = admin_url

        # Database setup
        self.db_engine = None
        self.session_factory = None
        if self.db_url:
            self.db_engine = create_async_engine(self.db_url)
            self.session_factory = sessionmaker(
                bind=self.db_engine, class_=AsyncSession, expire_on_commit=False
            )

            @self.fastapi_app.middleware("http")
            async def db_session_middleware(request: Request, call_next):
                if not self.session_factory:
                    return await call_next(request)

                async with self.session_factory() as session:
                    token = db_session_context.set(session)
                    try:
                        response = await call_next(request)
                    finally:
                        db_session_context.reset(token)
                return response

            @self.fastapi_app.on_event("shutdown")
            async def on_shutdown():
                if self.db_engine:
                    await self.db_engine.dispose()

        # Admin setup
        self.admin = None
        if self.enable_admin and self.db_engine:
            try:
                from .admin import FastMangoAdmin
                self.admin = FastMangoAdmin(self, admin_url=self.admin_url)
            except ImportError:
                print("Warning: SQLAdmin is not installed. Admin interface disabled.")
                self.admin = None
            except Exception as e:
                # Fail gracefully if admin setup fails
                print(f"Warning: Admin setup failed: {e}")
                self.admin = None

        # Placeholder for future engine/server instances
        self.llm_engine = None
        self.mcp_server = None

        if self.llm_config:
            # Logic to initialize the LLM engine will go here.
            pass
        if self.mcp_config:
            # Initialize the MCP server
            self.mcp_server = MCPServer(self.fastapi_app, self.mcp_config)

    def get(self, path: str, **kwargs):
        """Registers a GET route."""
        return self.fastapi_app.get(path, **kwargs)

    def post(self, path: str, **kwargs):
        """Registers a POST route."""
        return self.fastapi_app.post(path, **kwargs)

    def put(self, path: str, **kwargs):
        """Registers a PUT route."""
        return self.fastapi_app.put(path, **kwargs)

    def delete(self, path: str, **kwargs):
        """Registers a DELETE route."""
        return self.fastapi_app.delete(path, **kwargs)

    def patch(self, path: str, **kwargs):
        """Registers a PATCH route."""
        return self.fastapi_app.patch(path, **kwargs)

    def llm_endpoint(self, path: str, **kwargs):
        """
        Decorator to create an LLM-integrated endpoint.
        (Placeholder for future implementation)
        """
        def decorator(func):
            # The logic for the LLM-integrated endpoint will be implemented here.
            return func
        return decorator

    def mcp_tool(self, name: Optional[str] = None, **kwargs):
        """
        Decorator to register a function as an MCP tool.
        """
        from .mcp.decorators import mcp_tool as _mcp_tool
        return _mcp_tool(name, **kwargs)

    def include_router(self, router, **kwargs):
        """Includes a FastAPI router in the application."""
        self.fastapi_app.include_router(router, **kwargs)

    def mount_admin(self, path: str, admin_instance):
        """Mounts an admin instance at the specified path."""
        if admin_instance:
            self.fastapi_app.mount(path, admin_instance.asgi_app)
        else:
            raise RuntimeError("Admin interface is not enabled or not properly initialized")

    @property
    def asgi(self):
        """Provides access to the underlying ASGI application."""
        return self.fastapi_app
