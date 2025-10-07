import pytest
from unittest.mock import Mock

from fastmango.admin import Admin


@pytest.mark.unit
def test_admin_creation():
    """Test basic admin creation."""
    admin = Admin()
    
    assert admin is not None
    assert hasattr(admin, 'models')
    assert len(admin.models) == 0


@pytest.mark.unit
def test_admin_register_model():
    """Test model registration in admin."""
    admin = Admin()
    
    # Mock model class
    mock_model = Mock()
    mock_model.__name__ = "TestModel"
    
    admin.register_model(mock_model)
    
    assert len(admin.models) == 1
    assert "TestModel" in admin.models
    assert admin.models["TestModel"] == mock_model


@pytest.mark.unit
def test_admin_register_duplicate_model():
    """Test that registering the same model twice raises an error."""
    admin = Admin()
    
    # Mock model class
    mock_model = Mock()
    mock_model.__name__ = "TestModel"
    
    admin.register_model(mock_model)
    
    with pytest.raises(ValueError, match="Model TestModel is already registered"):
        admin.register_model(mock_model)


@pytest.mark.unit
def test_admin_unregister_model():
    """Test model unregistration from admin."""
    admin = Admin()
    
    # Mock model class
    mock_model = Mock()
    mock_model.__name__ = "TestModel"
    
    admin.register_model(mock_model)
    assert len(admin.models) == 1
    
    admin.unregister_model("TestModel")
    assert len(admin.models) == 0


@pytest.mark.unit
def test_admin_unregister_nonexistent_model():
    """Test that unregistering a non-existent model raises an error."""
    admin = Admin()
    
    with pytest.raises(ValueError, match="Model NonExistentModel is not registered"):
        admin.unregister_model("NonExistentModel")


@pytest.mark.unit
def test_admin_get_model():
    """Test getting a registered model."""
    admin = Admin()
    
    # Mock model class
    mock_model = Mock()
    mock_model.__name__ = "TestModel"
    
    admin.register_model(mock_model)
    
    retrieved_model = admin.get_model("TestModel")
    assert retrieved_model == mock_model


@pytest.mark.unit
def test_admin_get_nonexistent_model():
    """Test that getting a non-existent model returns None."""
    admin = Admin()
    
    retrieved_model = admin.get_model("NonExistentModel")
    assert retrieved_model is None