import typer
from .new import app as new_app
from .run import app as run_app
from .db import app as db_app
from .admin import app as admin_app
from .mcp import app as mcp_app

def version_callback(
    version: bool = typer.Option(False, "--version", help="Show version and exit")
):
    if version:
        from .. import __version__
        typer.echo(f"FastMango version: {__version__}")
        raise typer.Exit()

app = typer.Typer(
    name="fastmango",
    help="An AI-first web framework for modern Python developers.",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    callback=version_callback,
    invoke_without_command=True,
)

# Register the subcommands from other files.
app.add_typer(new_app, name="new")
app.add_typer(run_app, name="run")
app.add_typer(db_app, name="db")
app.add_typer(admin_app, name="admin")
app.add_typer(mcp_app, name="mcp")

@app.command()
def version():
    """
    Shows the version of the FastMango framework.
    """
    from .. import __version__
    typer.echo(f"FastMango version: {__version__}")

if __name__ == "__main__":
    app()
