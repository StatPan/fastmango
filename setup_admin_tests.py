"""
FastMango Admin Test Setup

This script helps set up the environment for running functional tests
and provides a readiness check for admin functionality testing.
"""

import sys
import subprocess
import importlib
import os

def check_dependency(module_name, package_name=None):
    """Check if a dependency is available."""
    if package_name is None:
        package_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} - Available")
        return True
    except ImportError:
        print(f"❌ {module_name} - Missing (install: pip install {package_name})")
        return False

def check_all_dependencies():
    """Check all required dependencies for admin testing."""
    print("🔍 Checking Dependencies for Admin Functional Tests")
    print("=" * 60)
    
    dependencies = [
        ("fastapi", "fastapi"),
        ("sqladmin", "sqladmin"),
        ("sqlmodel", "sqlmodel"),
        ("aiosqlite", "aiosqlite"),
        ("uvicorn", "uvicorn[standard]"),
        ("typer", "typer"),
        ("pydantic", "pydantic"),
        ("python_multipart", "python-multipart"),
    ]
    
    all_available = True
    for module, package in dependencies:
        if not check_dependency(module, package):
            all_available = False
    
    print("=" * 60)
    return all_available

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing Dependencies for Admin Testing")
    print("=" * 50)
    
    dependencies = [
        "fastapi",
        "sqladmin", 
        "sqlmodel",
        "aiosqlite",
        "uvicorn[standard]",
        "typer",
        "pydantic",
        "python-multipart",
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ {dep} installed successfully")
            else:
                print(f"❌ Failed to install {dep}: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout installing {dep}")
            return False
        except Exception as e:
            print(f"❌ Error installing {dep}: {e}")
            return False
    
    print("✅ All dependencies installed successfully")
    return True

def create_test_environment():
    """Create a test environment for admin functionality."""
    print("🏗️  Creating Test Environment")
    print("=" * 40)
    
    # Create test database directory
    test_dir = "test_data"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"✅ Created test directory: {test_dir}")
    
    # Create a simple test app
    test_app_content = '''
"""
Simple test app for admin functionality testing.
"""

from fastmango import MangoApp
from fastmango.models import Model
from sqlmodel import Field

class TestUser(Model, table=True):
    __tablename__ = "test_users"
    
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)

class TestPost(Model, table=True):
    __tablename__ = "test_posts"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int | None = Field(default=None, foreign_key="test_users.id")

# Create app with admin
app = MangoApp(
    title="Admin Test App",
    database_url="sqlite+aiosqlite:///test_data/admin_test.db",
    enable_admin=True,
    admin_url="/admin"
)

@app.get("/")
async def root():
    return {"message": "Admin Test App"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app.fastapi_app, host="127.0.0.1", port=8000)
'''
    
    with open("test_admin_app.py", "w") as f:
        f.write(test_app_content)
    
    print("✅ Created test admin app: test_admin_app.py")
    return True

def run_simple_test():
    """Run a simple test to verify admin functionality."""
    print("🧪 Running Simple Admin Test")
    print("=" * 40)
    
    try:
        # Import and test basic functionality
        sys.path.insert(0, 'src')
        
        from fastmango.app import MangoApp
        from fastmango.models import Model
        from sqlmodel import Field
        
        print("✅ Basic imports successful")
        
        # Create a simple test
        class SimpleTest(Model, table=True):
            __tablename__ = "simple_test"
            id: int | None = Field(default=None, primary_key=True)
            name: str
        
        print("✅ Test model created")
        
        # Create app with admin
        app = MangoApp(
            database_url="sqlite+aiosqlite:///test_data/simple_test.db",
            enable_admin=True
        )
        
        print("✅ App with admin created")
        
        if app.admin:
            print("✅ Admin interface initialized")
            
            # Register test model
            admin_view = app.admin.register_model(SimpleTest)
            print("✅ Model registered with admin")
            
            # Check registration
            if app.admin.is_model_registered(SimpleTest):
                print("✅ Model registration verified")
            else:
                print("❌ Model registration failed")
                return False
        else:
            print("❌ Admin not initialized")
            return False
        
        print("✅ Simple test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False

def run_functional_tests():
    """Run the full functional test suite."""
    print("🚀 Running Full Functional Test Suite")
    print("=" * 50)
    
    try:
        # Import and run functional tests
        import test_admin_functional
        
        result = test_admin_functional.run_functional_tests()
        return result
        
    except Exception as e:
        print(f"❌ Functional tests failed: {e}")
        return False

def main():
    """Main setup and test runner."""
    print("🎯 FastMango Admin Test Setup & Runner")
    print("=" * 50)
    
    # Check dependencies
    if not check_all_dependencies():
        print("\n❌ Some dependencies are missing.")
        print("Would you like to install them? (y/n)")
        
        try:
            response = input().strip().lower()
            if response in ['y', 'yes']:
                if not install_dependencies():
                    print("❌ Failed to install dependencies")
                    return False
            else:
                print("❌ Cannot proceed without dependencies")
                return False
        except KeyboardInterrupt:
            print("\n❌ Setup cancelled")
            return False
    
    # Create test environment
    if not create_test_environment():
        print("❌ Failed to create test environment")
        return False
    
    # Run simple test
    if not run_simple_test():
        print("❌ Simple test failed")
        return False
    
    # Ask if user wants to run full functional tests
    print("\n🚀 Simple test passed! Run full functional tests? (y/n)")
    try:
        response = input().strip().lower()
        if response in ['y', 'yes']:
            if not run_functional_tests():
                print("❌ Some functional tests failed")
                return False
    except KeyboardInterrupt:
        print("\n❌ Functional tests cancelled")
    
    print("\n🎉 Admin test setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: python test_admin_app.py")
    print("2. Visit: http://localhost:8000/admin")
    print("3. Test admin functionality manually")
    print("4. Run: python test_admin_functional.py")
    
    return True

if __name__ == "__main__":
    main()