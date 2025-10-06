import typer
from alembic.config import Config
from alembic import command
import os

app = typer.Typer()

def get_alembic_config():
    """Dynamically finds and returns the Alembic Config object."""
    # This assumes the command is run from the project root.
    # A more robust solution might search upwards for the alembic.ini file.
    alembic_cfg = Config("alembic.ini")
    return alembic_cfg

@app.command(name="revision", help="Create a new database revision (similar to makemigrations).")
def revision(message: str = typer.Option(None, "-m", "--message", help="Revision message.")):
    """Creates a new Alembic revision."""
    alembic_cfg = get_alembic_config()
    typer.echo("Creating new database revision...")
    command.revision(alembic_cfg, message=message, autogenerate=True)
    typer.echo("Revision created successfully.")

@app.command(name="upgrade", help="Apply migrations to the database (similar to migrate).")
def upgrade(revision: str = typer.Argument("head", help="The revision to upgrade to.")):
    """Applies migrations to the database."""
    alembic_cfg = get_alembic_config()
    typer.echo(f"Upgrading database to revision: {revision}")
    command.upgrade(alembic_cfg, revision)
    typer.echo("Database upgrade complete.")

if __name__ == "__main__":
    app()