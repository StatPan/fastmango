import typer
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
import os
import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

app = typer.Typer(
    name="db",
    help="Database management commands for FastMango applications.",
    add_completion=False,
)

def get_alembic_config(config_path: Optional[str] = None) -> Config:
    """
    Dynamically finds and returns the Alembic Config object.
    
    Args:
        config_path: Optional path to alembic.ini file
        
    Returns:
        Alembic Config object
    """
    if config_path:
        alembic_cfg = Config(config_path)
    else:
        # Search for alembic.ini in current directory and parent directories
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            ini_path = current_dir / "alembic.ini"
            if ini_path.exists():
                alembic_cfg = Config(str(ini_path))
                return alembic_cfg
            current_dir = current_dir.parent
        
        # Fallback to current directory
        alembic_cfg = Config("alembic.ini")
    
    return alembic_cfg

def get_database_url(config: Config) -> str:
    """Get database URL from Alembic config."""
    return config.get_main_option("sqlalchemy.url")

def get_current_revision(config: Config) -> Optional[str]:
    """Get current database revision."""
    try:
        db_url = get_database_url(config)
        # Create async engine for SQLite
        if db_url.startswith("sqlite"):
            # For SQLite, use sync engine
            engine = create_engine(db_url.replace("+aiosqlite", ""))
        else:
            # For other databases, use sync engine
            engine = create_engine(db_url)
        
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            return context.get_current_revision()
    except Exception:
        return None

def get_head_revision(config: Config) -> Optional[str]:
    """Get the latest revision available."""
    script_dir = ScriptDirectory.from_config(config)
    head = script_dir.get_current_head()
    return head

def get_migration_history(config: Config, limit: int = 10) -> List[Dict[str, Any]]:
    """Get migration history."""
    script_dir = ScriptDirectory.from_config(config)
    history = []
    
    for rev in script_dir.walk_revisions():
        history.append({
            "revision": rev.revision,
            "down_revision": rev.down_revision,
            "doc": rev.doc,
            "create_date": rev.create_date.strftime("%Y-%m-%d %H:%M:%S") if rev.create_date else None,
        })
    
    return history[:limit]

@app.command(name="revision", help="Create a new database revision (similar to makemigrations).")
def revision(
    message: str = typer.Option(None, "-m", "--message", help="Revision message."),
    autogenerate: bool = typer.Option(True, help="Auto-generate migration from model changes."),
    empty: bool = typer.Option(False, help="Create empty migration."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """
    Creates a new Alembic revision.
    
    Examples:
        fastmango db revision -m "Add user profile table"
        fastmango db revision -m "Custom migration" --empty
    """
    alembic_cfg = get_alembic_config(config_path)
    
    if empty:
        autogenerate = False
    
    if not message:
        message = typer.prompt("Enter revision message")
    
    typer.echo("🔄 Creating new database revision...")
    command.revision(alembic_cfg, message=message, autogenerate=autogenerate)
    typer.echo("✅ Revision created successfully.")
    
    # Show the created revision info
    history = get_migration_history(alembic_cfg, limit=1)
    if history:
        latest = history[0]
        typer.echo(f"📝 Revision: {latest['revision']}")
        typer.echo(f"📄 Message: {latest['doc']}")

@app.command(name="upgrade", help="Apply migrations to the database (similar to migrate).")
def upgrade(
    revision: str = typer.Argument("head", help="The revision to upgrade to."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """
    Applies migrations to the database.
    
    Examples:
        fastmango db upgrade
        fastmango db upgrade head
        fastmango db upgrade 2023_01_01_1200_initial
    """
    alembic_cfg = get_alembic_config(config_path)
    
    current_rev = get_current_revision(alembic_cfg)
    target_rev = revision if revision != "head" else get_head_revision(alembic_cfg)
    
    typer.echo(f"🔄 Upgrading database...")
    if current_rev:
        typer.echo(f"📍 Current revision: {current_rev}")
    else:
        typer.echo("📍 Current revision: None (database not initialized)")
    
    if target_rev:
        typer.echo(f"🎯 Target revision: {target_rev}")
    else:
        typer.echo("🎯 Target revision: head")
    
    try:
        command.upgrade(alembic_cfg, revision)
        typer.echo("✅ Database upgrade complete.")
        
        # Show new revision
        new_rev = get_current_revision(alembic_cfg)
        if new_rev:
            typer.echo(f"📍 New revision: {new_rev}")
    except Exception as e:
        typer.echo(f"❌ Upgrade failed: {e}", err=True)
        raise typer.Exit(1)

@app.command(name="downgrade", help="Rollback migrations to a previous revision.")
def downgrade(
    revision: str = typer.Argument("-1", help="The revision to downgrade to."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """
    Rollback migrations to a previous revision.
    
    Examples:
        fastmango db downgrade
        fastmango db downgrade -1
        fastmango db downgrade 2023_01_01_1200_initial
    """
    alembic_cfg = get_alembic_config(config_path)
    
    current_rev = get_current_revision(alembic_cfg)
    if not current_rev:
        typer.echo("❌ No migrations applied to database.", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"🔄 Downgrading database...")
    typer.echo(f"📍 Current revision: {current_rev}")
    typer.echo(f"🎯 Target revision: {revision}")
    
    try:
        command.downgrade(alembic_cfg, revision)
        typer.echo("✅ Database downgrade complete.")
        
        # Show new revision
        new_rev = get_current_revision(alembic_cfg)
        if new_rev:
            typer.echo(f"📍 New revision: {new_rev}")
        else:
            typer.echo("📍 New revision: None (database reset)")
    except Exception as e:
        typer.echo(f"❌ Downgrade failed: {e}", err=True)
        raise typer.Exit(1)

@app.command(name="status", help="Show current migration status.")
def status(config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file.")):
    """Show current migration status."""
    alembic_cfg = get_alembic_config(config_path)
    
    current_rev = get_current_revision(alembic_cfg)
    head_rev = get_head_revision(alembic_cfg)
    
    typer.echo("📊 Database Migration Status")
    typer.echo("=" * 40)
    typer.echo(f"📍 Current revision: {current_rev or 'None'}")
    typer.echo(f"🎯 Latest revision: {head_rev or 'None'}")
    
    if current_rev == head_rev:
        typer.echo("✅ Database is up to date")
    elif current_rev is None:
        typer.echo("⚠️  Database not initialized")
    else:
        typer.echo("⚠️  Database needs migration")
    
    # Show pending migrations
    if current_rev and head_rev and current_rev != head_rev:
        typer.echo("\n📋 Pending migrations:")
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        for rev in script_dir.walk_revisions():
            if rev.revision == current_rev:
                break
            typer.echo(f"  - {rev.revision}: {rev.doc or 'No description'}")

@app.command(name="history", help="Show migration history.")
def history(
    limit: int = typer.Option(10, help="Number of revisions to show."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """Show migration history."""
    alembic_cfg = get_alembic_config(config_path)
    history_list = get_migration_history(alembic_cfg, limit)
    
    if not history_list:
        typer.echo("No migrations found.")
        return
    
    typer.echo("📜 Migration History")
    typer.echo("=" * 40)
    
    for i, rev in enumerate(history_list, 1):
        status = "✅" if rev["revision"] == get_current_revision(alembic_cfg) else "⏳"
        typer.echo(f"{status} {rev['revision'][:12]}... - {rev['doc'] or 'No description'}")
        if rev["create_date"]:
            typer.echo(f"   📅 {rev['create_date']}")

@app.command(name="init", help="Initialize migration environment.")
def init(
    directory: str = typer.Option("migrations", help="Migration directory name."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """
    Initialize migration environment in a new project.
    
    Examples:
        fastmango db init
        fastmango db init --directory migrations
    """
    if Path("alembic.ini").exists():
        typer.echo("⚠️  Migration environment already initialized.", err=True)
        raise typer.Exit(1)
    
    try:
        # Initialize Alembic
        alembic_cfg = Config()
        command.init(alembic_cfg, directory)
        
        typer.echo("✅ Migration environment initialized successfully.")
        typer.echo(f"📁 Migration directory: {directory}")
        typer.echo("📝 Configuration file: alembic.ini")
        typer.echo("\nNext steps:")
        typer.echo("1. Review and update alembic.ini")
        typer.echo("2. Run 'fastmango db revision -m \"Initial migration\"'")
        typer.echo("3. Run 'fastmango db upgrade'")
    except Exception as e:
        typer.echo(f"❌ Initialization failed: {e}", err=True)
        raise typer.Exit(1)

@app.command(name="check", help="Check database connection and migration status.")
def check(config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file.")):
    """Check database connection and migration status."""
    alembic_cfg = get_alembic_config(config_path)
    
    typer.echo("🔍 Database Connection Check")
    typer.echo("=" * 40)
    
    # Check database connection
    try:
        db_url = get_database_url(alembic_cfg)
        typer.echo(f"🔗 Database URL: {db_url}")
        
        engine = create_engine(db_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            typer.echo("✅ Database connection: OK")
    except Exception as e:
        typer.echo(f"❌ Database connection: Failed - {e}", err=True)
        raise typer.Exit(1)
    
    # Check migration status
    current_rev = get_current_revision(alembic_cfg)
    head_rev = get_head_revision(alembic_cfg)
    
    typer.echo(f"📍 Current revision: {current_rev or 'None'}")
    typer.echo(f"🎯 Latest revision: {head_rev or 'None'}")
    
    if current_rev == head_rev:
        typer.echo("✅ Migration status: Up to date")
    elif current_rev is None:
        typer.echo("⚠️  Migration status: Not initialized")
    else:
        typer.echo("⚠️  Migration status: Needs upgrade")

@app.command(name="docs", help="Generate database schema documentation.")
def docs(
    output_dir: str = typer.Option("docs", help="Output directory for documentation."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """
    Generate comprehensive database schema documentation.
    
    This command generates documentation for all database models, including
    columns, relationships, indexes, and constraints. The documentation
    is saved in both JSON and Markdown formats.
    
    Examples:
        fastmango db docs
        fastmango db docs --output-dir documentation
        fastmango db docs --config-path custom_alembic.ini
    """
    alembic_cfg = get_alembic_config(config_path)
    
    try:
        # Import the schema documentation generator
        from ..db.schema_docs import generate_schema_docs
        
        # Create async engine
        db_url = get_database_url(alembic_cfg)
        engine = create_async_engine(db_url)
        
        typer.echo("📝 Generating database schema documentation...")
        typer.echo(f"📁 Output directory: {output_dir}")
        
        # Generate documentation
        async def generate_docs():
            return await generate_schema_docs(engine, output_dir)
        
        # Run the async function
        docs_data = asyncio.run(generate_docs())
        
        # Display summary
        models_count = len(docs_data.get('models', []))
        indexes_count = len(docs_data.get('indexes', []))
        constraints_count = len(docs_data.get('constraints', []))
        
        typer.echo("✅ Documentation generated successfully!")
        typer.echo(f"📊 Models documented: {models_count}")
        typer.echo(f"🔑 Indexes documented: {indexes_count}")
        typer.echo(f"🔒 Constraints documented: {constraints_count}")
        
        # Dispose engine
        asyncio.run(engine.dispose())
        
    except ImportError as e:
        typer.echo(f"❌ Failed to import schema documentation generator: {e}", err=True)
        typer.echo("Make sure the fastmango.db.schema_docs module is available.")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to generate documentation: {e}", err=True)
        raise typer.Exit(1)

@app.command(name="validate", help="Validate database schema and migrations.")
def validate(config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file.")):
    """
    Validate database schema and check for potential issues.
    
    This command performs various validation checks on the database schema
    and migrations to identify potential issues before they become problems.
    
    Examples:
        fastmango db validate
        fastmango db validate --config-path custom_alembic.ini
    """
    alembic_cfg = get_alembic_config(config_path)
    
    typer.echo("🔍 Database Schema Validation")
    typer.echo("=" * 40)
    
    # Check database connection
    try:
        db_url = get_database_url(alembic_cfg)
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # Check for common issues
            issues = []
            
            # Check 1: Tables without primary keys
            result = connection.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                AND name NOT IN (
                    SELECT DISTINCT tbl_name FROM sqlite_master 
                    WHERE type='table' AND sql LIKE '%PRIMARY KEY%'
                )
            """))
            
            tables_without_pk = [row[0] for row in result]
            if tables_without_pk:
                issues.append(f"Tables without primary keys: {', '.join(tables_without_pk)}")
            
            # Check 2: Foreign key constraints
            try:
                result = connection.execute(text("PRAGMA foreign_key_check"))
                fk_violations = result.fetchall()
                if fk_violations:
                    issues.append(f"Foreign key violations: {len(fk_violations)}")
            except:
                pass
            
            # Check 3: Unindexed foreign keys
            result = connection.execute(text("""
                SELECT sql FROM sqlite_master 
                WHERE type='table' AND sql LIKE '%FOREIGN KEY%'
            """))
            
            unindexed_fks = []
            for row in result:
                table_sql = row[0]
                if 'REFERENCES' in table_sql:
                    # This is a simplified check
                    unindexed_fks.append("Potential unindexed foreign key detected")
            
            if unindexed_fks:
                issues.extend(unindexed_fks[:3])  # Limit to 3 to avoid spam
            
            # Report results
            if not issues:
                typer.echo("✅ No schema validation issues found.")
            else:
                typer.echo("⚠️  Schema validation issues found:")
                for issue in issues:
                    typer.echo(f"  - {issue}")
            
            # Check migration status
            current_rev = get_current_revision(alembic_cfg)
            head_rev = get_head_revision(alembic_cfg)
            
            if current_rev != head_rev:
                typer.echo("⚠️  Database is not up to date with migrations.")
                typer.echo("   Run 'fastmango db upgrade' to apply pending migrations.")
            
    except Exception as e:
        typer.echo(f"❌ Validation failed: {e}", err=True)
        raise typer.Exit(1)

@app.command(name="migrate-data", help="Run data migrations.")
def migrate_data(
    migration_name: Optional[str] = typer.Option(None, help="Specific migration to run."),
    rollback: bool = typer.Option(False, help="Rollback the last migration."),
    status: bool = typer.Option(False, help="Show migration status."),
    config_path: Optional[str] = typer.Option(None, help="Path to alembic.ini file."),
):
    """
    Run data migrations for transforming data during schema changes.
    
    Data migrations are different from schema migrations - they transform
    existing data while preserving the schema structure.
    
    Examples:
        fastmango db migrate-data                    # Run all pending migrations
        fastmango db migrate-data --status          # Show migration status
        fastmango db migrate-data --rollback        # Rollback last migration
        fastmango db migrate-data --migration-name add_user_email_verification
    """
    alembic_cfg = get_alembic_config(config_path)
    
    try:
        # Import migration utilities
        from ..db.migration_utils import MigrationRunner
        from ..db.migration_utils import (
            AddUserEmailVerificationMigration,
            MigrateUserPasswordsMigration,
        )
        
        # Create async engine
        db_url = get_database_url(alembic_cfg)
        engine = create_async_engine(db_url)
        
        # Create migration runner
        runner = MigrationRunner(engine)
        
        # Register example migrations
        runner.register_migration(AddUserEmailVerificationMigration())
        runner.register_migration(MigrateUserPasswordsMigration())
        
        async def run_migration_command():
            if status:
                # Show migration status
                status_info = await runner.get_migration_status()
                
                typer.echo("📊 Data Migration Status")
                typer.echo("=" * 40)
                typer.echo(f"Total migrations: {status_info['total_migrations']}")
                typer.echo(f"Applied: {status_info['applied_count']}")
                typer.echo(f"Pending: {status_info['pending_count']}")
                
                if status_info['applied_migrations']:
                    typer.echo("\n✅ Applied migrations:")
                    for migration in status_info['applied_migrations']:
                        typer.echo(f"  - {migration}")
                
                if status_info['pending_migrations']:
                    typer.echo("\n⏳ Pending migrations:")
                    for migration in status_info['pending_migrations']:
                        typer.echo(f"  - {migration}")
                
            elif rollback:
                # Rollback last migration
                success = await runner.rollback_last_migration()
                if success:
                    typer.echo("✅ Last migration rolled back successfully.")
                else:
                    typer.echo("⚠️  No migration to rollback.")
                
            elif migration_name:
                # Run specific migration
                for migration in runner.migrations:
                    if migration.name == migration_name:
                        success = await runner.run_migration(migration)
                        if success:
                            typer.echo(f"✅ Migration '{migration_name}' applied successfully.")
                        else:
                            typer.echo(f"⏭️  Migration '{migration_name}' was already applied.")
                        break
                else:
                    typer.echo(f"❌ Migration '{migration_name}' not found.", err=True)
                    raise typer.Exit(1)
                
            else:
                # Run all pending migrations
                typer.echo("🔄 Running pending data migrations...")
                applied_count = await runner.run_pending_migrations()
                
                if applied_count > 0:
                    typer.echo(f"✅ Applied {applied_count} data migration(s).")
                else:
                    typer.echo("ℹ️  No pending data migrations.")
            
            # Dispose engine
            await engine.dispose()
        
        # Run the async command
        asyncio.run(run_migration_command())
        
    except ImportError as e:
        typer.echo(f"❌ Failed to import migration utilities: {e}", err=True)
        typer.echo("Make sure the fastmango.db.migration_utils module is available.")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Data migration failed: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()