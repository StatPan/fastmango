"""
Database Schema Documentation Generator for FastMango

This module provides functionality to generate comprehensive documentation
for database schemas, including models, relationships, and migrations.
"""

import inspect
from typing import Dict, List, Any, Optional, Type
from pathlib import Path
import json
from datetime import datetime

from sqlalchemy import inspect as sqlalchemy_inspect
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.sql import text
from sqlmodel import SQLModel, Field

from ..models import Model


class SchemaDocumentationGenerator:
    """
    Generates comprehensive documentation for database schemas.
    """
    
    def __init__(self, engine: AsyncEngine):
        """
        Initialize the schema documentation generator.
        
        Args:
            engine: Async SQLAlchemy engine
        """
        self.engine = engine
    
    async def generate_schema_docs(self, output_dir: str = "docs") -> Dict[str, Any]:
        """
        Generate comprehensive schema documentation.
        
        Args:
            output_dir: Directory to save documentation files
            
        Returns:
            Dictionary containing all generated documentation
        """
        docs = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "fastmango_version": "0.1.0"
            },
            "models": await self.get_models_documentation(),
            "relationships": await self.get_relationships_documentation(),
            "indexes": await self.get_indexes_documentation(),
            "constraints": await self.get_constraints_documentation(),
            "database_info": await self.get_database_info()
        }
        
        # Save documentation files
        await self.save_documentation(docs, output_dir)
        
        return docs
    
    async def get_models_documentation(self) -> List[Dict[str, Any]]:
        """
        Get documentation for all models.
        
        Returns:
            List of model documentation dictionaries
        """
        models_docs = []
        
        # Import FastMango models
        try:
            from ..models import User
            
            # List of models to document
            models_to_document = [User]
            
            for model_class in models_to_document:
                model_doc = await self.get_model_documentation(model_class)
                if model_doc:
                    models_docs.append(model_doc)
                    
        except ImportError as e:
            print(f"Warning: Could not import models: {e}")
        
        return models_docs
    
    async def get_model_documentation(self, model_class: Type[SQLModel]) -> Optional[Dict[str, Any]]:
        """
        Get documentation for a specific model.
        
        Args:
            model_class: SQLModel class
            
        Returns:
            Model documentation dictionary
        """
        try:
            # Get table information
            table = model_class.__table__
            
            # Get columns documentation
            columns = []
            for column in table.columns:
                # Handle foreign keys properly
                foreign_key = None
                if column.foreign_keys:
                    # Take the first foreign key if there are multiple
                    fk = list(column.foreign_keys)[0]
                    foreign_key = str(fk.target_fullname)
                
                column_doc = {
                    "name": column.name,
                    "type": str(column.type),
                    "nullable": column.nullable,
                    "primary_key": column.primary_key,
                    "unique": column.unique,
                    "default": str(column.default) if column.default else None,
                    "foreign_key": foreign_key,
                    "description": column.doc if hasattr(column, 'doc') else None
                }
                columns.append(column_doc)
            
            # Get model docstring
            docstring = model_class.__doc__ or "No description available"
            
            return {
                "name": model_class.__name__,
                "table_name": table.name,
                "description": docstring.strip(),
                "columns": columns,
                "column_count": len(columns)
            }
            
        except Exception as e:
            print(f"Error getting documentation for {model_class.__name__}: {e}")
            return None
    
    async def get_relationships_documentation(self) -> List[Dict[str, Any]]:
        """
        Get documentation for all relationships.
        
        Returns:
            List of relationship documentation dictionaries
        """
        relationships = []
        
        # This would require more complex introspection
        # For now, return a placeholder
        return relationships
    
    async def get_indexes_documentation(self) -> List[Dict[str, Any]]:
        """
        Get documentation for all indexes.
        
        Returns:
            List of index documentation dictionaries
        """
        indexes = []
        
        async with self.engine.connect() as conn:
            # Get indexes from database
            try:
                result = await conn.execute(text("""
                    SELECT 
                        tablename,
                        indexname,
                        indexdef
                    FROM pg_indexes 
                    WHERE schemaname = 'public'
                    ORDER BY tablename, indexname
                """))
                
                for row in result:
                    indexes.append({
                        "table": row.tablename,
                        "name": row.indexname,
                        "definition": row.indexdef
                    })
            except Exception:
                # Fallback for SQLite or other databases
                pass
        
        return indexes
    
    async def get_constraints_documentation(self) -> List[Dict[str, Any]]:
        """
        Get documentation for all constraints.
        
        Returns:
            List of constraint documentation dictionaries
        """
        constraints = []
        
        async with self.engine.connect() as conn:
            try:
                # Get constraints from database
                result = await conn.execute(text("""
                    SELECT 
                        tc.table_name,
                        tc.constraint_name,
                        tc.constraint_type,
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    LEFT JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.table_schema = tc.table_schema
                    WHERE tc.table_schema = 'public'
                    ORDER BY tc.table_name, tc.constraint_name
                """))
                
                for row in result:
                    constraints.append({
                        "table": row.table_name,
                        "name": row.constraint_name,
                        "type": row.constraint_type,
                        "column": row.column_name,
                        "foreign_table": row.foreign_table_name,
                        "foreign_column": row.foreign_column_name
                    })
            except Exception:
                # Fallback for SQLite or other databases
                pass
        
        return constraints
    
    async def get_database_info(self) -> Dict[str, Any]:
        """
        Get general database information.
        
        Returns:
            Database information dictionary
        """
        info = {}
        
        async with self.engine.connect() as conn:
            # Get database version
            try:
                result = await conn.execute(text("SELECT sqlite_version()"))
                info["version"] = f"SQLite {result.scalar()}"
            except Exception:
                try:
                    result = await conn.execute(text("SELECT version()"))
                    info["version"] = result.scalar()
                except Exception:
                    info["version"] = "Unknown"
            
            # Get table count
            try:
                result = await conn.execute(text("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """))
                info["table_count"] = result.scalar()
            except Exception:
                try:
                    result = await conn.execute(text("""
                        SELECT COUNT(*) FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """))
                    info["table_count"] = result.scalar()
                except Exception:
                    info["table_count"] = 0
        
        return info
    
    async def save_documentation(self, docs: Dict[str, Any], output_dir: str) -> None:
        """
        Save documentation to files.
        
        Args:
            docs: Documentation dictionary
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save JSON documentation
        json_file = output_path / "schema_docs.json"
        with open(json_file, 'w') as f:
            json.dump(docs, f, indent=2, default=str)
        
        # Save Markdown documentation
        await self.save_markdown_docs(docs, output_path)
        
        print(f"✅ Documentation saved to {output_dir}")
        print(f"📄 JSON: {json_file}")
        print(f"📝 Markdown: {output_path / 'schema_docs.md'}")
    
    async def save_markdown_docs(self, docs: Dict[str, Any], output_path: Path) -> None:
        """
        Save documentation as Markdown.
        
        Args:
            docs: Documentation dictionary
            output_path: Output directory path
        """
        md_content = []
        
        # Header
        md_content.append("# Database Schema Documentation")
        md_content.append("")
        md_content.append(f"Generated on: {docs['metadata']['generated_at']}")
        md_content.append("")
        
        # Database Info
        db_info = docs['database_info']
        md_content.append("## Database Information")
        md_content.append("")
        md_content.append(f"- **Version**: {db_info.get('version', 'Unknown')}")
        md_content.append(f"- **Table Count**: {db_info.get('table_count', 0)}")
        md_content.append("")
        
        # Models
        md_content.append("## Models")
        md_content.append("")
        
        for model in docs['models']:
            md_content.append(f"### {model['name']}")
            md_content.append("")
            md_content.append(f"**Table**: `{model['table_name']}`")
            md_content.append("")
            md_content.append(f"**Description**: {model['description']}")
            md_content.append("")
            
            md_content.append("#### Columns")
            md_content.append("")
            md_content.append("| Name | Type | Nullable | Primary Key | Unique | Default | Foreign Key |")
            md_content.append("|------|------|----------|-------------|--------|---------|-------------|")
            
            for column in model['columns']:
                nullable = "✓" if column['nullable'] else "✗"
                primary_key = "✓" if column['primary_key'] else "✗"
                unique = "✓" if column['unique'] else "✗"
                default = column['default'] or "-"
                foreign_key = column['foreign_key'] or "-"
                
                md_content.append(f"| {column['name']} | {column['type']} | {nullable} | {primary_key} | {unique} | {default} | {foreign_key} |")
            
            md_content.append("")
        
        # Indexes
        if docs['indexes']:
            md_content.append("## Indexes")
            md_content.append("")
            
            for index in docs['indexes']:
                md_content.append(f"### {index['name']}")
                md_content.append("")
                md_content.append(f"**Table**: `{index['table']}`")
                md_content.append("")
                md_content.append(f"**Definition**: `{index['definition']}`")
                md_content.append("")
        
        # Constraints
        if docs['constraints']:
            md_content.append("## Constraints")
            md_content.append("")
            
            for constraint in docs['constraints']:
                md_content.append(f"### {constraint['name']}")
                md_content.append("")
                md_content.append(f"**Table**: `{constraint['table']}`")
                md_content.append(f"**Type**: {constraint['type']}")
                md_content.append(f"**Column**: `{constraint['column']}`")
                if constraint['foreign_table']:
                    md_content.append(f"**Foreign Table**: `{constraint['foreign_table']}`")
                    md_content.append(f"**Foreign Column**: `{constraint['foreign_column']}`")
                md_content.append("")
        
        # Save markdown file
        md_file = output_path / "schema_docs.md"
        with open(md_file, 'w') as f:
            f.write('\n'.join(md_content))


async def generate_schema_docs(engine: AsyncEngine, output_dir: str = "docs") -> Dict[str, Any]:
    """
    Convenience function to generate schema documentation.
    
    Args:
        engine: Async SQLAlchemy engine
        output_dir: Output directory for documentation
        
    Returns:
        Generated documentation dictionary
    """
    generator = SchemaDocumentationGenerator(engine)
    return await generator.generate_schema_docs(output_dir)