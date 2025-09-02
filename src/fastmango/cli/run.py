import typer
import uvicorn
import sys
import os
from pathlib import Path

app = typer.Typer(name="run", help="Run the FastMango development server.")

@app.callback(invoke_without_command=True)
def run(
    host: str = typer.Option("127.0.0.1", help="The host to bind to."),
    port: int = typer.Option(8000, help="The port to bind to."),
    reload: bool = typer.Option(True, help="Enable auto-reloading."),
):
    """
    Starts the development server for a FastMango project.
    """
    # This assumes there is a `main.py` file with an `app` variable
    # in the current directory. A more robust solution might search for the app.
    app_module = "main"
    app_variable = "app"

    # Check if main.py exists
    if not Path(f"{app_module}.py").exists():
        typer.secho(
            f"Error: Could not find `{app_module}.py`. "
            f"Make sure you are in a FastMango project directory.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    # Add current directory to the path to allow uvicorn to find the module.
    sys.path.insert(0, os.getcwd())

    typer.secho(f"🔥 Starting FastMango dev server...", fg=typer.colors.CYAN)
    typer.secho(f"🌐 Listening on http://{host}:{port}", fg=typer.colors.CYAN)
    typer.secho(f"🔄 Auto-reload is {'on' if reload else 'off'}", fg=typer.colors.CYAN)

    uvicorn.run(
        f"{app_module}:{app_variable}.asgi",
        host=host,
        port=port,
        reload=reload,
    )
