from typing import ClassVar, Generic, List, Optional, Type, TypeVar
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from contextvars import ContextVar

# This context variable will hold the session for the current request.
# It will be managed by a middleware in the MangoApp.
db_session_context: ContextVar[Optional[AsyncSession]] = ContextVar("db_session_context", default=None)


T = TypeVar("T", bound="Model")


class Manager(Generic[T]):
    """
    A Django-style manager for handling database operations asynchronously.
    """
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def _get_session(self) -> AsyncSession:
        """Retrieves the database session from the context variable."""
        session = db_session_context.get()
        if session is None:
            raise RuntimeError(
                "Database session not available in context. "
                "Ensure the database middleware is set up correctly in your MangoApp."
            )
        return session

    async def all(self) -> List[T]:
        """Retrieves all objects from the database."""
        session = self._get_session()
        result = await session.execute(select(self.model_class))
        return result.scalars().all()

    async def filter(self, **kwargs) -> List[T]:
        """Filters objects based on keyword arguments (exact match)."""
        session = self._get_session()
        conditions = [getattr(self.model_class, k) == v for k, v in kwargs.items()]
        statement = select(self.model_class).where(*conditions)
        result = await session.execute(statement)
        return result.scalars().all()

    async def get(self, **kwargs) -> Optional[T]:
        """Retrieivs a single object or None if not found."""
        session = self._get_session()
        statement = select(self.model_class).filter_by(**kwargs)
        result = await session.execute(statement)
        return result.scalars().first()

    async def get_or_404(self, **kwargs) -> T:
        """Retrieivs a single object or raises an HTTPException if not found."""
        obj = await self.get(**kwargs)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{self.model_class.__name__} not found.")
        return obj

    async def create(self, **kwargs) -> T:
        """Creates and saves a new object."""
        session = self._get_session()
        instance = self.model_class(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


class Model(SQLModel):
    """
    A base model class that provides Django-style ORM features.
    All data models in a FastMango application should inherit from this class.
    """
    objects: ClassVar[Manager]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Attach a manager instance to the class itself.
        cls.objects = Manager(cls)

    async def save(self):
        """Saves the current instance to the database."""
        session = self.objects._get_session()
        session.add(self)
        await session.commit()
        await session.refresh(self)

    async def delete(self):
        """Deletes the current instance from the database."""
        session = self.objects._get_session()
        await session.delete(self)
        await session.commit()

# --- Add a simple User model for testing ---
class User(Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    password_hash: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)