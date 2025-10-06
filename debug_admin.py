"""
Debug script to check why admin is not being initialized.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_admin_initialization():
    """Debug admin initialization process."""
    print("🔍 Debugging Admin Initialization")
    print("=" * 40)
    
    try:
        # Import required modules
        from fastmango.app import MangoApp
        from fastmango.models import Model
        from sqlmodel import Field
        
        print("✅ Imports successful")
        
        # Define test model
        class DebugTest(Model, table=True):
            __tablename__ = "debug_test"
            id: int | None = Field(default=None, primary_key=True)
            name: str
        
        print("✅ Test model defined")
        
        # Create app with explicit database URL
        app = MangoApp(
            title="Debug Test App",
            database_url="sqlite+aiosqlite:///test_data/debug_test.db",
            enable_admin=True,
            admin_url="/admin"
        )
        
        print(f"📊 App created with database_url: {app.db_url}")
        print(f"📊 App db_engine: {app.db_engine}")
        print(f"📊 App enable_admin: {app.enable_admin}")
        print(f"📊 App admin: {app.admin}")
        
        # Check if admin is available
        if hasattr(app, 'admin') and app.admin is not None:
            print("✅ Admin is initialized")
            
            # Test model registration
            admin_view = app.admin.register_model(DebugTest)
            print("✅ Model registered with admin")
            
            # Check registration
            if app.admin.is_model_registered(DebugTest):
                print("✅ Model registration verified")
                return True
            else:
                print("❌ Model registration failed")
                return False
        else:
            print("❌ Admin is not initialized")
            
            # Try to understand why
            print("\n🔍 Checking admin availability...")
            
            # Check if admin module can be imported
            try:
                from fastmango.admin import FastMangoAdmin
                print("✅ FastMangoAdmin can be imported")
            except ImportError as e:
                print(f"❌ Cannot import FastMangoAdmin: {e}")
                return False
            
            # Check if ADMIN_AVAILABLE is set
            try:
                from fastmango.app import ADMIN_AVAILABLE
                print(f"📊 ADMIN_AVAILABLE: {ADMIN_AVAILABLE}")
            except:
                print("❌ ADMIN_AVAILABLE not found")
            
            # Try to manually create admin
            try:
                admin = FastMangoAdmin(app)
                print("✅ Manual admin creation successful")
                app.admin = admin
                
                # Now test model registration
                admin_view = app.admin.register_model(DebugTest)
                print("✅ Model registered with manual admin")
                
                return True
            except Exception as e:
                print(f"❌ Manual admin creation failed: {e}")
                return False
    
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_with_real_app():
    """Test admin with a real app structure."""
    print("\n🧪 Testing Admin with Real App Structure")
    print("=" * 50)
    
    try:
        # Import the test app we created
        import test_admin_app
        
        print("✅ Test app imported")
        
        # Check if admin is initialized in the test app
        if hasattr(test_admin_app.app, 'admin') and test_admin_app.app.admin is not None:
            print("✅ Admin is initialized in test app")
            
            # Check registered models
            registered_models = test_admin_app.app.admin.get_registered_models()
            print(f"📊 Registered models: {[m.__name__ for m in registered_models]}")
            
            return True
        else:
            print("❌ Admin is not initialized in test app")
            return False
    
    except Exception as e:
        print(f"❌ Real app test failed: {e}")
        return False

if __name__ == "__main__":
    debug_admin_initialization()
    test_admin_with_real_app()