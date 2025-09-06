from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from contextvars import ContextVar

# This context variable will hold the session for the current request.
# It will be managed by a middleware in the MangoApp.
db_session_context: ContextVar[Optional[AsyncSession]] = ContextVar("db_session_context", default=None)
