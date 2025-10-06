"""
FastMango Admin CLI Commands

Provides command-line interface for managing FastMango admin functionality.
"""

import typer
from typing import Optional
import uvicorn
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

async def create_admin_user(username: str, email: str, password: str, database_url: Optional[str] = None) -> bool:
    """Create an admin user with the given credentials."""
    try:
        from ..app import MangoApp
        from ..models import User
        
        # Create app with database
        mango_app = MangoApp(database_url=database_url)
        
        if mango_app.db_engine is None:
            typer.echo("❌ Database is not configured.", err=True)
            return False
        
        # Check if user already exists
        async with mango_app.session_factory() as session:
            # Import the context variable
            from ..models import db_session_context
            
            # Set the session context
            token = db_session_context.set(session)
            try:
                # Check if user already exists
                existing_user = await User.objects.get(username=username)
                if existing_user:
                    typer.echo(f"❌ User '{username}' already exists.", err=True)
                    return False
                
                # Check if email already exists
                existing_email = await User.objects.get(email=email)
                if existing_email:
                    typer.echo(f"❌ Email '{email}' already exists.", err=True)
                    return False
                
                # Create the user with hashed password
                user = await User.objects.create(
                    username=username,
                    email=email,
                    password_hash=hash_password(password),
                    is_active=True,
                )
                
                typer.echo(f"✅ Admin user '{username}' created successfully!")
                typer.echo(f"📧 Email: {email}")
                typer.echo(f"🔑 You can now log in at /admin")
                return True
                
            finally:
                db_session_context.reset(token)
                
    except ImportError as e:
        typer.echo(f"❌ Failed to import FastMango: {e}", err=True)
        return False
    except Exception as e:
        typer.echo(f"❌ Failed to create admin user: {e}", err=True)
        return False

app = typer.Typer(
    name="admin", 
    help="Admin interface commands for FastMango applications.",
    add_completion=False,
)


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    reload: bool = typer.Option(False, help="Enable auto-reload for development"),
    admin_url: str = typer.Option("/admin", help="URL path for admin interface"),
):
    """
    Start the FastMango application with admin interface.
    
    This command starts your FastMango application with the admin interface
    enabled at the specified URL.
    
    Example:
        fastmango admin serve
        fastmango admin serve --host 0.0.0.0 --port 8080
        fastmango admin serve --reload
    """
    try:
        # Import the application
        from ..app import MangoApp
        
        # Try to create app with admin enabled
        mango_app = MangoApp(
            title="FastMango Application",
            enable_admin=True,
            admin_url=admin_url,
        )
        
        if mango_app.admin is None:
            typer.echo(
                "❌ Admin interface could not be initialized. "
                "Please ensure you have a database configured and SQLAdmin installed.",
                err=True
            )
            raise typer.Exit(1)
        
        typer.echo(f"🚀 Starting FastMango with admin interface...")
        typer.echo(f"📊 Admin interface: http://{host}:{port}{admin_url}")
        typer.echo(f"🌐 API docs: http://{host}:{port}/docs")
        typer.echo(f"🔄 Auto-reload: {'enabled' if reload else 'disabled'}")
        typer.echo("Press Ctrl+C to stop the server")
        
        # Start the server
        uvicorn.run(
            mango_app.fastapi_app,
            host=host,
            port=port,
            reload=reload,
        )
        
    except ImportError as e:
        typer.echo(f"❌ Failed to import FastMango: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to start server: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def createuser(
    username: str = typer.Option(..., prompt=True, help="Admin username"),
    email: str = typer.Option(..., prompt=True, help="Admin email"),
    password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password"),
    database_url: Optional[str] = typer.Option(None, help="Database URL"),
):
    """
    Create an admin user for the application.
    
    This command creates a superuser with admin privileges.
    You'll be prompted for the required information.
    
    Example:
        fastmango admin createuser
        fastmango admin createuser --database-url sqlite:///admin.db
    """
    import asyncio
    
    # Run the async function
    result = asyncio.run(create_admin_user(username, email, password, database_url))
    
    if not result:
        raise typer.Exit(1)


@app.command()
def check():
    """
    Check admin interface configuration and status.
    
    This command checks if the admin interface is properly configured
    and shows information about registered models.
    
    Example:
        fastmango admin check
    """
    try:
        from ..app import MangoApp
        
        # Create app to check configuration
        mango_app = MangoApp(enable_admin=True)
        
        typer.echo("🔍 FastMango Admin Configuration Check")
        typer.echo("=" * 40)
        
        # Check admin availability
        if mango_app.admin is None:
            typer.echo("❌ Admin interface: Not available")
            typer.echo("   Possible causes:")
            typer.echo("   - SQLAdmin not installed")
            typer.echo("   - Database not configured")
            typer.echo("   - Admin disabled in configuration")
        else:
            typer.echo("✅ Admin interface: Available")
            typer.echo(f"📍 Admin URL: {mango_app.admin_url}")
            
            # Check registered models
            registered_models = mango_app.admin.get_registered_models()
            if registered_models:
                typer.echo(f"📊 Registered models: {len(registered_models)}")
                for model in registered_models:
                    typer.echo(f"   - {model.__name__}")
            else:
                typer.echo("⚠️  No models registered")
                typer.echo("   Make sure your models inherit from fastmango.Model")
        
        # Check database
        if mango_app.db_engine:
            typer.echo("✅ Database: Configured")
        else:
            typer.echo("❌ Database: Not configured")
        
        typer.echo("=" * 40)
        
    except ImportError as e:
        typer.echo(f"❌ Failed to import FastMango: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Configuration check failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def setup(
    database_url: Optional[str] = typer.Option(None, help="Database URL"),
    admin_url: str = typer.Option("/admin", help="URL path for admin interface"),
):
    """
    Interactive setup for FastMango admin interface.
    
    This command guides you through setting up the admin interface
    for your FastMango application.
    
    Example:
        fastmango admin setup
        fastmango admin setup --database-url sqlite:///myapp.db
    """
    typer.echo("🚀 FastMango Admin Setup")
    typer.echo("=" * 30)
    
    # Ask for database URL if not provided
    if not database_url:
        database_url = typer.prompt(
            "Database URL", 
            default="sqlite+aiosqlite:///fastmango.db"
        )
    
    try:
        from ..app import MangoApp
        
        # Create app with specified configuration
        mango_app = MangoApp(
            database_url=database_url,
            enable_admin=True,
            admin_url=admin_url,
        )
        
        if mango_app.admin is None:
            typer.echo("❌ Failed to initialize admin interface.", err=True)
            raise typer.Exit(1)
        
        typer.echo("✅ Admin interface configured successfully!")
        typer.echo(f"📍 Admin URL: {admin_url}")
        typer.echo(f"🗄️  Database: {database_url}")
        
        # Ask if user wants to create an admin user
        create_user = typer.confirm("Would you like to create an admin user now?")
        if create_user:
            # Get user credentials
            username = typer.prompt("Admin username")
            email = typer.prompt("Admin email")
            password = typer.prompt("Admin password", hide_input=True, confirmation_prompt=True)
            
            # Create the user
            import asyncio
            result = asyncio.run(create_admin_user(username, email, password, database_url))
            if not result:
                raise typer.Exit(1)
        
        typer.echo("\n🎉 Setup complete!")
        typer.echo(f"Start your app with: fastmango admin serve --admin-url {admin_url}")
        
    except ImportError as e:
        typer.echo(f"❌ Failed to import FastMango: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Setup failed: {e}", err=True)
        raise typer.Exit(1)