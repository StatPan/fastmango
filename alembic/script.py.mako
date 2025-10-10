"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union
import logging

from alembic import op
import sqlalchemy as sa
 ${imports if imports else ""}

# Configure logging
logger = logging.getLogger('alembic')
logger.setLevel(logging.INFO)

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema.
    
    This migration was auto-generated on ${create_date}.
    Review the changes below before applying.
    """
    logger.info(f"Applying migration {revision}: ${message}")
    
    try:
        ${upgrades if upgrades else "pass"}
        logger.info(f"Successfully applied migration {revision}")
    except Exception as e:
        logger.error(f"Failed to apply migration {revision}: {e}")
        raise


def downgrade() -> None:
    """Downgrade schema.
    
    This migration rolls back the changes made in revision ${revision}.
    """
    logger.info(f"Rolling back migration {revision}: ${message}")
    
    try:
        ${downgrades if downgrades else "pass"}
        logger.info(f"Successfully rolled back migration {revision}")
    except Exception as e:
        logger.error(f"Failed to rollback migration {revision}: {e}")
        raise


# Migration metadata
MIGRATION_INFO = {
    "revision": ${repr(up_revision)},
    "message": ${repr(message)},
    "created_at": ${repr(create_date)},
    "author": "FastMango",
    "auto_generated": True,
}