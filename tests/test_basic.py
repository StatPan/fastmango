import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel, select, Field
import os
from typing import Optional

from fastmango.app import MangoApp

# Set up the database URL for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

# Define a User model for testing
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    username: str

# Create a new MangoApp instance for testing
app = MangoApp(database_url=TEST_DATABASE_URL)

# Add a root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Hello, FastMango!"}

# Create the test database engine
engine = create_async_engine(TEST_DATABASE_URL)


@pytest.fixture(name="session")
async def session_fixture():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


def test_basic_app():
    with TestClient(app.fastapi_app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, FastMango!"}


@pytest.mark.anyio
async def test_with_sqlite(session: AsyncSession):
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    statement = select(User).where(User.email == "test@example.com")
    result = await session.execute(statement)
    retrieved_user = result.scalar_one_or_none()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"


@pytest.mark.anyio
async def test_user(session: AsyncSession):
    user_data = {"email": "test2@example.com", "username": "testuser2"}
    new_user = User(**user_data)
    session.add(new_user)
    await session.commit()

    statement = select(User).where(User.email == "test2@example.com")
    result = await session.execute(statement)
    retrieved_user = result.scalar_one_or_none()
    assert retrieved_user is not None
    assert retrieved_user.email == "test2@example.com"
