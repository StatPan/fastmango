"""
Simple Test for FastMango Admin Integration

This test file verifies the basic structure of the admin integration
without requiring all dependencies to be installed.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test that basic FastMango modules can be imported."""
    try:
        from fastmango.app import MangoApp
        from fastmango.models import Model
        print("✅ Basic FastMango imports successful")
        return True
    except ImportError as e:
        print(f"❌ Failed to import basic FastMango modules: {e}")
        return False

def test_admin_module_structure():
    """Test that admin module files exist and have basic structure."""
    admin_dir = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'admin')
    
    # Check that admin directory exists
    if not os.path.exists(admin_dir):
        print("❌ Admin directory does not exist")
        return False
    
    # Check that required files exist
    required_files = ['__init__.py', 'base.py', 'views.py']
    for file in required_files:
        file_path = os.path.join(admin_dir, file)
        if not os.path.exists(file_path):
            print(f"❌ Admin file {file} does not exist")
            return False
        print(f"✅ Admin file {file} exists")
    
    return True

def test_admin_init_content():
    """Test that admin __init__.py has correct content."""
    init_file = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'admin', '__init__.py')
    
    with open(init_file, 'r') as f:
        content = f.read()
    
    # Check that it exports the expected classes
    if 'FastMangoAdmin' in content and 'ModelAdmin' in content:
        print("✅ Admin __init__.py exports expected classes")
        return True
    else:
        print("❌ Admin __init__.py does not export expected classes")
        return False

def test_admin_base_content():
    """Test that admin base.py has FastMangoAdmin class."""
    base_file = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'admin', 'base.py')
    
    with open(base_file, 'r') as f:
        content = f.read()
    
    # Check that it contains the FastMangoAdmin class
    if 'class FastMangoAdmin' in content:
        print("✅ Admin base.py contains FastMangoAdmin class")
        return True
    else:
        print("❌ Admin base.py does not contain FastMangoAdmin class")
        return False

def test_admin_views_content():
    """Test that admin views.py has ModelAdmin class."""
    views_file = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'admin', 'views.py')
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Check that it contains the ModelAdmin class
    if 'class ModelAdmin' in content:
        print("✅ Admin views.py contains ModelAdmin class")
        return True
    else:
        print("❌ Admin views.py does not contain ModelAdmin class")
        return False

def test_app_integration():
    """Test that MangoApp has admin integration code."""
    app_file = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'app.py')
    
    with open(app_file, 'r') as f:
        content = f.read()
    
    # Check that it contains admin-related code
    if ('enable_admin' in content and 
        'FastMangoAdmin' in content and 
        'admin_url' in content):
        print("✅ MangoApp has admin integration code")
        return True
    else:
        print("❌ MangoApp does not have admin integration code")
        return False

def test_cli_integration():
    """Test that CLI has admin commands."""
    cli_main_file = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'cli', 'main.py')
    admin_cli_file = os.path.join(os.path.dirname(__file__), 'src', 'fastmango', 'cli', 'admin.py')
    
    # Check main CLI file
    with open(cli_main_file, 'r') as f:
        main_content = f.read()
    
    # Check admin CLI file exists
    if not os.path.exists(admin_cli_file):
        print("❌ Admin CLI file does not exist")
        return False
    
    with open(admin_cli_file, 'r') as f:
        admin_content = f.read()
    
    # Check that admin is registered in main CLI
    if 'admin_app' in main_content and 'add_typer(admin_app' in main_content:
        print("✅ Admin CLI is registered in main CLI")
    else:
        print("❌ Admin CLI is not registered in main CLI")
        return False
    
    # Check that admin CLI has commands
    if ('def serve' in admin_content and 
        'def createuser' in admin_content and 
        'def check' in admin_content):
        print("✅ Admin CLI has expected commands")
        return True
    else:
        print("❌ Admin CLI does not have expected commands")
        return False

def test_pyproject_toml():
    """Test that pyproject.toml has SQLAdmin dependency."""
    pyproject_file = os.path.join(os.path.dirname(__file__), 'pyproject.toml')
    
    with open(pyproject_file, 'r') as f:
        content = f.read()
    
    # Check that SQLAdmin is in dependencies
    if 'sqladmin' in content:
        print("✅ pyproject.toml has SQLAdmin dependency")
        return True
    else:
        print("❌ pyproject.toml does not have SQLAdmin dependency")
        return False

def run_simple_tests():
    """Run all simple admin integration tests."""
    print("🧪 Running FastMango Admin Simple Tests")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_admin_module_structure,
        test_admin_init_content,
        test_admin_base_content,
        test_admin_views_content,
        test_app_integration,
        test_cli_integration,
        test_pyproject_toml,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All simple tests passed!")
        print("✅ Task #16: SQLAdmin Integration Foundation - Basic Structure Complete")
        print("\n📋 Next Steps:")
        print("1. Install dependencies: pip install sqladmin")
        print("2. Test with real database: python -m fastmango admin serve")
        print("3. Verify admin interface at /admin")
    else:
        print("❌ Some tests failed")
        return False
    
    return True

if __name__ == "__main__":
    run_simple_tests()