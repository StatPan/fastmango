import pytest
from fastapi.testclient import TestClient
from sqlmodel import Field

from fastmango.app import MangoApp
from fastmango.models import Model
from fastmango.admin import Admin


class TestUser(Model, table=True):
    """Test user model for integration testing."""
    __tablename__ = "test_users"
    
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    is_active: bool = Field(default=True)


class TestPost(Model, table=True):
    """Test post model for integration testing."""
    __tablename__ = "test_posts"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int | None = Field(default=None, foreign_key="test_users.id")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_admin_integration_with_app(set_db_context):
    """Test admin integration with FastMango app."""
    # Create app with database URL to enable admin
    app = MangoApp(database_url="sqlite+aiosqlite:///:memory:")
    
    # The admin should be automatically initialized
    # Register model with the internal admin
    if app.admin:
        app.admin.register_model(TestUser)
    
    # Mount admin to app
    app.mount_admin("/admin", app.admin)
    
    # Create test client
    client = TestClient(app.fastapi_app)
    
    # Test admin home page
    response = client.get("/admin/")
    assert response.status_code == 200
    assert "FastAPI Admin" in response.text
    
    # Test model list page
    response = client.get("/admin/testuser/")
    assert response.status_code == 200
    assert "TestUser" in response.text
    
    # Test create form page
    response = client.get("/admin/testuser/create")
    assert response.status_code == 200
    assert "Create" in response.text


@pytest.mark.asyncio
@pytest.mark.integration
async def test_admin_crud_operations(set_db_context):
    """Test complete CRUD operations through admin interface."""
    # Create app with database URL to enable admin
    app = MangoApp(database_url="sqlite+aiosqlite:///:memory:")
    
    # The admin should be automatically initialized
    # Register model with the internal admin
    if app.admin:
        app.admin.register_model(TestUser)
    
    # Mount admin to app
    app.mount_admin("/admin", app.admin)
    
    # Create test client
    client = TestClient(app.fastapi_app)
    
    # Create user through admin
    create_data = {
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True
    }
    
    response = client.post("/admin/testuser/create", data=create_data)
    assert response.status_code == 302  # Redirect after successful creation
    
    # Verify user was created
    users = await TestUser.objects.all()
    assert len(users) == 1
    assert users[0].username == "testuser"
    assert users[0].email == "test@example.com"
    
    # Test user list page shows created user
    response = client.get("/admin/testuser/")
    assert response.status_code == 200
    assert "testuser" in response.text
    
    # Test edit page
    user = users[0]
    response = client.get(f"/admin/testuser/{user.id}/edit")
    assert response.status_code == 200
    assert "testuser" in response.text
    
    # Update user through admin
    update_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "is_active": False
    }
    
    response = client.post(f"/admin/testuser/{user.id}/edit", data=update_data)
    assert response.status_code == 302  # Redirect after successful update
    
    # Verify user was updated
    updated_user = await TestUser.objects.get(id=user.id)
    assert updated_user.username == "updateduser"
    assert updated_user.email == "updated@example.com"
    assert updated_user.is_active is False
    
    # Test delete user
    response = client.post(f"/admin/testuser/{user.id}/delete")
    assert response.status_code == 302  # Redirect after successful deletion
    
    # Verify user was deleted
    deleted_user = await TestUser.objects.get(id=user.id)
    assert deleted_user is None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_admin_with_multiple_models(set_db_context):
    """Test admin with multiple registered models."""
    # Create app with database URL to enable admin
    app = MangoApp(database_url="sqlite+aiosqlite:///:memory:")
    
    # The admin should be automatically initialized
    # Register models with the internal admin
    if app.admin:
        app.admin.register_model(TestUser)
        app.admin.register_model(TestPost)
    
    # Mount admin to app
    app.mount_admin("/admin", app.admin)
    
    # Create test client
    client = TestClient(app.fastapi_app)
    
    # Test admin home page shows both models
    response = client.get("/admin/")
    assert response.status_code == 200
    assert "TestUser" in response.text
    assert "TestPost" in response.text
    
    # Test both model list pages work
    response = client.get("/admin/testuser/")
    assert response.status_code == 200
    
    response = client.get("/admin/testpost/")
    assert response.status_code == 200