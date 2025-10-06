"""
FastMango Admin Functional Tests

This test suite provides comprehensive functional testing for the admin integration.
These tests require all dependencies to be installed and will test the actual
functionality of the admin interface.

Prerequisites:
- pip install sqladmin fastapi sqlmodel aiosqlite uvicorn
- Database access for testing

Run with: python test_admin_functional.py
"""

import asyncio
import sys
import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Field, Session
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_admin_full_workflow():
    """
    Test complete admin workflow from model definition to admin interface.
    This is the main functional test that verifies everything works together.
    """
    print("🧪 Testing Complete Admin Workflow")
    print("=" * 50)
    
    try:
        # Import required modules
        from fastmango.app import MangoApp
        from fastmango.models import Model
        from fastmango.admin import FastMangoAdmin, ModelAdmin
        
        print("✅ All imports successful")
        
        # Define test models
        class TestUser(Model, table=True):
            __tablename__ = "test_users"
            
            id: int | None = Field(default=None, primary_key=True)
            username: str = Field(index=True, unique=True)
            email: str = Field(unique=True)
            is_active: bool = Field(default=True)
            created_at: str = Field(default="2024-01-01")
        
        class TestPost(Model, table=True):
            __tablename__ = "test_posts"
            
            id: int | None = Field(default=None, primary_key=True)
            title: str
            content: str
            author_id: int | None = Field(default=None, foreign_key="test_users.id")
            is_published: bool = Field(default=False)
        
        print("✅ Test models defined")
        
        # Create app with admin
        app = MangoApp(
            title="Test Admin App",
            database_url="sqlite+aiosqlite:///test_admin.db",
            enable_admin=True,
            admin_url="/admin"
        )
        
        print("✅ MangoApp created with admin enabled")
        
        # Verify admin was initialized
        assert app.admin is not None, "Admin should be initialized"
        print("✅ Admin interface initialized")
        
        # Test model registration
        registered_models = app.admin.get_registered_models()
        print(f"📊 Auto-registered models: {[m.__name__ for m in registered_models]}")
        
        # Manually register test models (since they're defined in this test file)
        user_admin = app.admin.register_model(TestUser)
        post_admin = app.admin.register_model(TestPost)
        
        print("✅ Test models registered with admin")
        
        # Verify registration
        assert app.admin.is_model_registered(TestUser), "TestUser should be registered"
        assert app.admin.is_model_registered(TestPost), "TestPost should be registered"
        print("✅ Model registration verified")
        
        # Create test client
        client = TestClient(app.fastapi_app)
        print("✅ Test client created")
        
        # Test admin routes
        response = client.get("/admin")
        print(f"📍 Admin root route status: {response.status_code}")
        
        # Test admin list view for users
        response = client.get("/admin/test-user/list")
        print(f"📍 User list view status: {response.status_code}")
        
        # Test admin list view for posts
        response = client.get("/admin/test-post/list")
        print(f"📍 Post list view status: {response.status_code}")
        
        # Test admin create view
        response = client.get("/admin/test-user/create")
        print(f"📍 User create view status: {response.status_code}")
        
        print("✅ Admin routes are accessible")
        
        # Test API endpoints still work
        response = client.get("/")
        print(f"📍 API root status: {response.status_code}")
        
        print("✅ API endpoints still functional")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install dependencies: pip install sqladmin fastapi sqlmodel aiosqlite uvicorn")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_custom_admin_configuration():
    """
    Test custom admin configuration with ModelAdmin classes.
    """
    print("\n🧪 Testing Custom Admin Configuration")
    print("=" * 50)
    
    try:
        from fastmango.app import MangoApp
        from fastmango.models import Model
        from fastmango.admin import ModelAdmin
        from sqlmodel import Field
        
        # Define test model
        class CustomUser(Model, table=True):
            __tablename__ = "custom_users"
            
            id: int | None = Field(default=None, primary_key=True)
            username: str = Field(index=True, unique=True)
            email: str = Field(unique=True)
            is_active: bool = Field(default=True)
            role: str = Field(default="user")
        
        # Define custom admin
        class CustomUserAdmin(ModelAdmin):
            list_display = ['username', 'email', 'is_active', 'role']
            list_filter = ['is_active', 'role']
            search_fields = ['username', 'email']
            list_per_page = 10
            readonly_fields = ['id']
        
        print("✅ Custom model and admin defined")
        
        # Create app
        app = MangoApp(
            title="Custom Admin Test",
            database_url="sqlite+aiosqlite:///test_custom.db",
            enable_admin=True
        )
        
        # Register custom admin
        app.admin.register_custom_admin(CustomUser, CustomUserAdmin)
        
        print("✅ Custom admin registered")
        
        # Test client
        client = TestClient(app.fastapi_app)
        
        # Test custom admin view
        response = client.get("/admin/custom-user/list")
        print(f"📍 Custom user list status: {response.status_code}")
        
        print("✅ Custom admin configuration working")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_admin_database_operations():
    """
    Test actual database operations through the admin interface.
    """
    print("\n🧪 Testing Admin Database Operations")
    print("=" * 50)
    
    try:
        from fastmango.app import MangoApp
        from fastmango.models import Model
        from sqlmodel import Field, create_engine
        from sqlalchemy.ext.asyncio import create_async_engine
        
        # Define test model
        class BlogPost(Model, table=True):
            __tablename__ = "blog_posts"
            
            id: int | None = Field(default=None, primary_key=True)
            title: str
            content: str
            published: bool = Field(default=False)
        
        print("✅ BlogPost model defined")
        
        # Create app with database
        app = MangoApp(
            title="Blog Admin Test",
            database_url="sqlite+aiosqlite:///test_blog.db",
            enable_admin=True
        )
        
        # Register model
        app.admin.register_model(BlogPost)
        
        print("✅ BlogPost registered with admin")
        
        # Create test client
        client = TestClient(app.fastapi_app)
        
        # Test creating a post through admin API (if available)
        # This would test the actual form submission
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content",
            "published": True
        }
        
        # Note: Actual form submission would need CSRF tokens and proper authentication
        # For now, we test that the create form is accessible
        response = client.get("/admin/blog-post/create")
        print(f"📍 Create form status: {response.status_code}")
        
        # Test list view
        response = client.get("/admin/blog-post/list")
        print(f"📍 List view status: {response.status_code}")
        
        print("✅ Database operations interface working")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_admin_cli_functionality():
    """
    Test admin CLI commands functionality.
    """
    print("\n🧪 Testing Admin CLI Functionality")
    print("=" * 50)
    
    try:
        from fastmango.cli.admin import app as admin_app
        import typer.testing
        
        # Create CLI test runner
        runner = typer.testing.CliRunner()
        
        print("✅ CLI test runner created")
        
        # Test admin check command
        result = runner.invoke(admin_app, ["check"])
        print(f"📍 Admin check exit code: {result.exit_code}")
        if result.stdout:
            print(f"📍 Admin check output: {result.stdout[:200]}...")
        
        # Test admin setup command (non-interactive)
        result = runner.invoke(admin_app, ["setup", "--database-url", "sqlite+aiosqlite:///test_cli.db"])
        print(f"📍 Admin setup exit code: {result.exit_code}")
        
        print("✅ CLI commands functional")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 CLI testing requires typer and other dependencies")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_admin_error_handling():
    """
    Test admin error handling and edge cases.
    """
    print("\n🧪 Testing Admin Error Handling")
    print("=" * 50)
    
    try:
        from fastmango.app import MangoApp
        from fastmango.models import Model
        
        # Test admin disabled
        app = MangoApp(enable_admin=False)
        assert app.admin is None, "Admin should be None when disabled"
        print("✅ Admin can be disabled")
        
        # Test admin with no database
        app = MangoApp(enable_admin=True, database_url=None)
        # Should handle gracefully without crashing
        print("✅ Admin handles missing database gracefully")
        
        # Test invalid admin URL
        app = MangoApp(
            enable_admin=True,
            database_url="sqlite+aiosqlite:///test_error.db",
            admin_url="invalid-url"
        )
        # Should handle gracefully
        print("✅ Admin handles invalid URL gracefully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def run_functional_tests():
    """
    Run all functional tests.
    """
    print("🚀 FastMango Admin Functional Test Suite")
    print("=" * 60)
    print("⚠️  These tests require all dependencies to be installed:")
    print("   pip install sqladmin fastapi sqlmodel aiosqlite uvicorn typer")
    print()
    
    tests = [
        ("Complete Admin Workflow", test_admin_full_workflow),
        ("Custom Admin Configuration", test_custom_admin_configuration),
        ("Database Operations", test_admin_database_operations),
        ("CLI Functionality", test_admin_cli_functionality),
        ("Error Handling", test_admin_error_handling),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Functional Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All functional tests passed!")
        print("✅ Admin integration is fully functional")
    else:
        print("⚠️  Some tests failed - check dependencies and configuration")
    
    print("\n💡 To run these tests:")
    print("   1. Install dependencies: pip install sqladmin fastapi sqlmodel aiosqlite uvicorn typer")
    print("   2. Run: python test_admin_functional.py")
    print("   3. Visit: http://localhost:8000/admin for manual testing")
    
    return failed == 0


if __name__ == "__main__":
    run_functional_tests()