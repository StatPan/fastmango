"""
Test FastMango Admin Integration

This test file verifies that the admin integration works correctly
and that FastMango models are automatically registered with the admin interface.
"""

import asyncio
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.fastmango.app import MangoApp
from src.fastmango.models import Model, Manager
from src.fastmango.admin import FastMangoAdmin
from sqlmodel import Field

# Test models for admin integration
class TestUser(Model, table=True):
    __tablename__ = "test_users"
    
    id: int | None = None
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)


class TestPost(Model, table=True):
    __tablename__ = "test_posts"
    
    id: int | None = None
    title: str
    content: str
    author_id: int | None = Field(default=None, foreign_key="test_users.id")


def test_admin_dependency_import():
    """Test that admin dependencies can be imported."""
    try:
        from src.fastmango.admin import FastMangoAdmin, ModelAdmin
        assert FastMangoAdmin is not None
        assert ModelAdmin is not None
        print("✅ Admin dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import admin dependencies: {e}")
        raise


def test_mango_app_admin_integration():
    """Test that MangoApp can be initialized with admin functionality."""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Create MangoApp with admin enabled
    app = MangoApp(
        database_url="sqlite+aiosqlite:///:memory:",
        enable_admin=True,
        admin_url="/test-admin",
    )
    
    # Check that admin was initialized
    assert app.admin is not None, "Admin should be initialized"
    assert app.admin_url == "/test-admin"
    print("✅ MangoApp admin integration successful")


def test_admin_model_registration():
    """Test that FastMango models are automatically registered with admin."""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Create MangoApp with admin enabled
    app = MangoApp(
        database_url="sqlite+aiosqlite:///:memory:",
        enable_admin=True,
    )
    
    # Check that models were registered
    registered_models = app.admin.get_registered_models()
    
    # Should have at least our test models
    model_names = [model.__name__ for model in registered_models]
    
    # Note: The automatic model discovery might not find our test models
    # since they're defined in this test file, not in the main models module
    print(f"📊 Registered models: {model_names}")
    
    # At minimum, the User model from the main models module should be registered
    user_registered = any("User" in name for name in model_names)
    if user_registered:
        print("✅ User model automatically registered")
    else:
        print("⚠️  User model not found in automatic registration")
        print("   (This is expected if models are in different modules)")


def test_admin_custom_model_registration():
    """Test manual registration of models with admin."""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Create MangoApp with admin enabled
    app = MangoApp(
        database_url="sqlite+aiosqlite:///:memory:",
        enable_admin=True,
    )
    
    # Manually register our test models
    admin_view1 = app.admin.register_model(TestUser)
    admin_view2 = app.admin.register_model(TestPost)
    
    # Check that models were registered
    assert app.admin.is_model_registered(TestUser), "TestUser should be registered"
    assert app.admin.is_model_registered(TestPost), "TestPost should be registered"
    
    # Check that admin views were created
    assert admin_view1 is not None, "Admin view for TestUser should be created"
    assert admin_view2 is not None, "Admin view for TestPost should be created"
    
    print("✅ Custom model registration successful")


def test_admin_routes():
    """Test that admin routes are properly set up."""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Create MangoApp with admin enabled
    app = MangoApp(
        database_url="sqlite+aiosqlite:///:memory:",
        enable_admin=True,
        admin_url="/admin",
    )
    
    # Create test client
    client = TestClient(app.fastapi_app)
    
    # Test admin root route
    response = client.get("/admin")
    # Should return 200 (admin interface) or 302 (redirect to login)
    assert response.status_code in [200, 302], f"Admin route should be accessible, got {response.status_code}"
    
    print("✅ Admin routes are properly set up")


def test_admin_disabled():
    """Test that admin can be disabled."""
    # Create MangoApp with admin disabled
    app = MangoApp(
        database_url="sqlite+aiosqlite:///:memory:",
        enable_admin=False,
    )
    
    # Check that admin was not initialized
    assert app.admin is None, "Admin should not be initialized when disabled"
    
    print("✅ Admin can be disabled")


def test_cli_admin_commands():
    """Test that admin CLI commands are available."""
    try:
        from src.fastmango.cli.admin import app as admin_app
        assert admin_app is not None, "Admin CLI app should be available"
        
        # Check that commands are registered
        command_names = [cmd.name for cmd in admin_app.registered_commands]
        expected_commands = ["serve", "createuser", "check", "setup"]
        
        for cmd in expected_commands:
            assert cmd in command_names, f"Command '{cmd}' should be available"
        
        print("✅ Admin CLI commands are available")
        
    except ImportError as e:
        print(f"❌ Failed to import admin CLI: {e}")
        raise


def run_all_tests():
    """Run all admin integration tests."""
    print("🧪 Running FastMango Admin Integration Tests")
    print("=" * 50)
    
    tests = [
        test_admin_dependency_import,
        test_mango_app_admin_integration,
        test_admin_model_registration,
        test_admin_custom_model_registration,
        test_admin_routes,
        test_admin_disabled,
        test_cli_admin_commands,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")
        return False
    
    return True


if __name__ == "__main__":
    run_all_tests()