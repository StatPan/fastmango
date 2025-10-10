"""
Database Migration Utilities for FastMango

This module provides utilities for data migration and transformation
during database schema changes.
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime
import json
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import text, select, update, delete
from sqlmodel import SQLModel

from ..models import Model, db_session_context


class DataMigration:
    """
    Base class for data migrations.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a data migration.
        
        Args:
            name: Migration name
            description: Migration description
        """
        self.name = name
        self.description = description
        self.created_at = datetime.now()
    
    async def up(self, session: AsyncSession) -> None:
        """
        Apply the migration.
        
        Args:
            session: Database session
        """
        raise NotImplementedError("Subclasses must implement the up method")
    
    async def down(self, session: AsyncSession) -> None:
        """
        Rollback the migration.
        
        Args:
            session: Database session
        """
        raise NotImplementedError("Subclasses must implement the down method")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert migration to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }


class MigrationRunner:
    """
    Runs and manages data migrations.
    """
    
    def __init__(self, engine: AsyncEngine):
        """
        Initialize the migration runner.
        
        Args:
            engine: Async SQLAlchemy engine
        """
        self.engine = engine
        self.migrations: List[DataMigration] = []
        self._migration_table_created = False
    
    def register_migration(self, migration: DataMigration) -> None:
        """
        Register a migration.
        
        Args:
            migration: Migration to register
        """
        self.migrations.append(migration)
    
    async def ensure_migration_table(self) -> None:
        """Ensure the migration tracking table exists."""
        if self._migration_table_created:
            return
        
        async with self.engine.begin() as conn:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS fastmango_data_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP NOT NULL
                )
            """))
        
        self._migration_table_created = True
    
    async def get_applied_migrations(self) -> List[str]:
        """
        Get list of applied migration names.
        
        Returns:
            List of applied migration names
        """
        await self.ensure_migration_table()
        
        async with self.engine.connect() as conn:
            result = await conn.execute(text(
                "SELECT name FROM fastmango_data_migrations ORDER BY applied_at"
            ))
            return [row[0] for row in result]
    
    async def is_migration_applied(self, migration_name: str) -> bool:
        """
        Check if a migration has been applied.
        
        Args:
            migration_name: Migration name to check
            
        Returns:
            True if migration is applied
        """
        applied_migrations = await self.get_applied_migrations()
        return migration_name in applied_migrations
    
    async def mark_migration_applied(self, migration: DataMigration) -> None:
        """
        Mark a migration as applied.
        
        Args:
            migration: Migration to mark
        """
        await self.ensure_migration_table()
        
        async with self.engine.begin() as conn:
            await conn.execute(text("""
                INSERT INTO fastmango_data_migrations (name, description, created_at)
                VALUES (:name, :description, :created_at)
            """), {
                "name": migration.name,
                "description": migration.description,
                "created_at": migration.created_at
            })
    
    async def mark_migration_rolled_back(self, migration_name: str) -> None:
        """
        Mark a migration as rolled back.
        
        Args:
            migration_name: Migration name to mark
        """
        await self.ensure_migration_table()
        
        async with self.engine.begin() as conn:
            await conn.execute(text(
                "DELETE FROM fastmango_data_migrations WHERE name = :name"
            ), {"name": migration_name})
    
    async def run_migration(self, migration: DataMigration) -> bool:
        """
        Run a single migration.
        
        Args:
            migration: Migration to run
            
        Returns:
            True if migration was applied
        """
        if await self.is_migration_applied(migration.name):
            print(f"⏭️  Migration '{migration.name}' already applied, skipping.")
            return False
        
        print(f"🔄 Running migration: {migration.name}")
        
        try:
            async with self.engine.begin() as conn:
                async with AsyncSession(conn) as session:
                    # Set session context
                    token = db_session_context.set(session)
                    try:
                        await migration.up(session)
                        await session.commit()
                    finally:
                        db_session_context.reset(token)
            
            await self.mark_migration_applied(migration)
            print(f"✅ Migration '{migration.name}' applied successfully.")
            return True
            
        except Exception as e:
            print(f"❌ Migration '{migration.name}' failed: {e}")
            raise
    
    async def rollback_migration(self, migration: DataMigration) -> bool:
        """
        Rollback a single migration.
        
        Args:
            migration: Migration to rollback
            
        Returns:
            True if migration was rolled back
        """
        if not await self.is_migration_applied(migration.name):
            print(f"⚠️  Migration '{migration.name}' not applied, cannot rollback.")
            return False
        
        print(f"🔄 Rolling back migration: {migration.name}")
        
        try:
            async with self.engine.begin() as conn:
                async with AsyncSession(conn) as session:
                    # Set session context
                    token = db_session_context.set(session)
                    try:
                        await migration.down(session)
                        await session.commit()
                    finally:
                        db_session_context.reset(token)
            
            await self.mark_migration_rolled_back(migration.name)
            print(f"✅ Migration '{migration.name}' rolled back successfully.")
            return True
            
        except Exception as e:
            print(f"❌ Rollback of '{migration.name}' failed: {e}")
            raise
    
    async def run_pending_migrations(self) -> int:
        """
        Run all pending migrations.
        
        Returns:
            Number of migrations applied
        """
        applied_count = 0
        
        for migration in self.migrations:
            if await self.run_migration(migration):
                applied_count += 1
        
        return applied_count
    
    async def rollback_last_migration(self) -> bool:
        """
        Rollback the last applied migration.
        
        Returns:
            True if a migration was rolled back
        """
        applied_migrations = await self.get_applied_migrations()
        if not applied_migrations:
            print("⚠️  No migrations to rollback.")
            return False
        
        last_migration_name = applied_migrations[-1]
        
        # Find the migration object
        for migration in self.migrations:
            if migration.name == last_migration_name:
                return await self.rollback_migration(migration)
        
        print(f"❌ Migration '{last_migration_name}' not found in registered migrations.")
        return False
    
    async def get_migration_status(self) -> Dict[str, Any]:
        """
        Get migration status.
        
        Returns:
            Migration status dictionary
        """
        applied_migrations = await self.get_applied_migrations()
        pending_migrations = [
            m for m in self.migrations 
            if m.name not in applied_migrations
        ]
        
        return {
            "total_migrations": len(self.migrations),
            "applied_count": len(applied_migrations),
            "pending_count": len(pending_migrations),
            "applied_migrations": applied_migrations,
            "pending_migrations": [m.name for m in pending_migrations]
        }


class DataTransformer:
    """
    Utility for transforming data during migrations.
    """
    
    @staticmethod
    async def transform_table(
        session: AsyncSession,
        table_name: str,
        transformations: Dict[str, Callable[[Any], Any]]
    ) -> int:
        """
        Transform data in a table.
        
        Args:
            session: Database session
            table_name: Table name
            transformations: Dictionary of column transformations
            
        Returns:
            Number of rows transformed
        """
        # Get all data
        result = await session.execute(text(f"SELECT * FROM {table_name}"))
        rows = result.fetchall()
        
        if not rows:
            return 0
        
        # Get column names
        columns = result.keys()
        
        transformed_count = 0
        for row in rows:
            # Create update data
            update_data = {}
            for column_name, transform_func in transformations.items():
                if column_name in columns:
                    old_value = getattr(row, column_name)
                    new_value = transform_func(old_value)
                    if new_value != old_value:
                        update_data[column_name] = new_value
            
            if update_data:
                # Build update query
                set_clauses = [f"{k} = :{k}" for k in update_data.keys()]
                update_query = text(f"""
                    UPDATE {table_name} 
                    SET {', '.join(set_clauses)}
                    WHERE id = :id
                """)
                
                update_data["id"] = row.id
                await session.execute(update_query, update_data)
                transformed_count += 1
        
        return transformed_count
    
    @staticmethod
    async def copy_table_data(
        session: AsyncSession,
        source_table: str,
        target_table: str,
        column_mapping: Dict[str, str],
        filter_clause: Optional[str] = None
    ) -> int:
        """
        Copy data from one table to another.
        
        Args:
            session: Database session
            source_table: Source table name
            target_table: Target table name
            column_mapping: Dictionary mapping source columns to target columns
            filter_clause: Optional WHERE clause
            
        Returns:
            Number of rows copied
        """
        # Build column lists
        source_columns = list(column_mapping.keys())
        target_columns = list(column_mapping.values())
        
        # Build INSERT query
        insert_query = f"""
            INSERT INTO {target_table} ({', '.join(target_columns)})
            SELECT {', '.join(source_columns)}
            FROM {source_table}
        """
        
        if filter_clause:
            insert_query += f" WHERE {filter_clause}"
        
        result = await session.execute(text(insert_query))
        return result.rowcount
    
    @staticmethod
    async def backup_table(
        session: AsyncSession,
        table_name: str,
        backup_suffix: str = "_backup"
    ) -> str:
        """
        Create a backup of a table.
        
        Args:
            session: Database session
            table_name: Table to backup
            backup_suffix: Suffix for backup table name
            
        Returns:
            Backup table name
        """
        backup_table = f"{table_name}{backup_suffix}"
        
        # Drop backup table if it exists
        await session.execute(text(f"DROP TABLE IF EXISTS {backup_table}"))
        
        # Create backup
        await session.execute(text(f"""
            CREATE TABLE {backup_table} AS SELECT * FROM {table_name}
        """))
        
        return backup_table


# Example migrations
class AddUserEmailVerificationMigration(DataMigration):
    """Example migration to add email verification to users."""
    
    def __init__(self):
        super().__init__(
            "add_user_email_verification",
            "Add email verification fields to user table"
        )
    
    async def up(self, session: AsyncSession) -> None:
        """Add email verification columns."""
        await session.execute(text("""
            ALTER TABLE user ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
        """))
        await session.execute(text("""
            ALTER TABLE user ADD COLUMN email_verification_token VARCHAR(255)
        """))
        await session.execute(text("""
            ALTER TABLE user ADD COLUMN email_verification_expires TIMESTAMP
        """))
    
    async def down(self, session: AsyncSession) -> None:
        """Remove email verification columns."""
        await session.execute(text("""
            ALTER TABLE user DROP COLUMN email_verified
        """))
        await session.execute(text("""
            ALTER TABLE user DROP COLUMN email_verification_token
        """))
        await session.execute(text("""
            ALTER TABLE user DROP COLUMN email_verification_expires
        """))


class MigrateUserPasswordsMigration(DataMigration):
    """Example migration to migrate password hashes."""
    
    def __init__(self):
        super().__init__(
            "migrate_user_passwords",
            "Migrate user passwords to new hashing algorithm"
        )
    
    async def up(self, session: AsyncSession) -> None:
        """Migrate passwords to new hash."""
        # This is a simplified example
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Get all users
        result = await session.execute(text("SELECT id, password_hash FROM user"))
        users = result.fetchall()
        
        for user in users:
            if user.password_hash and not user.password_hash.startswith("$2b$"):
                # Rehash with bcrypt
                new_hash = pwd_context.hash(user.password_hash)
                await session.execute(text("""
                    UPDATE user SET password_hash = :new_hash WHERE id = :id
                """), {"new_hash": new_hash, "id": user.id})
    
    async def down(self, session: AsyncSession) -> None:
        """Rollback password migration."""
        # In a real scenario, you'd need to store old hashes
        pass