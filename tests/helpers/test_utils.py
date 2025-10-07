from typing import Any, Dict, List, Type
from sqlalchemy.ext.asyncio import AsyncSession

from fastmango.models import Model


async def create_test_model(
    model_class: Type[Model],
    **kwargs: Any
) -> Model:
    """Create a test model instance with given parameters."""
    return await model_class.objects.create(**kwargs)


async def create_test_models(
    model_class: Type[Model],
    count: int,
    **base_kwargs: Any
) -> List[Model]:
    """Create multiple test model instances."""
    models = []
    for i in range(count):
        kwargs = base_kwargs.copy()
        # Add index to string fields to ensure uniqueness
        for key, value in kwargs.items():
            if isinstance(value, str):
                kwargs[key] = f"{value}_{i}"
        
        model = await create_test_model(model_class, **kwargs)
        models.append(model)
    
    return models


async def clear_model_data(model_class: Type[Model]) -> None:
    """Clear all data for a specific model using bulk delete."""
    # Use bulk delete for better performance instead of N+1 queries
    await model_class.objects.delete_all()


async def setup_test_data(
    models_data: Dict[Type[Model], List[Dict[str, Any]]]
) -> Dict[Type[Model], List[Model]]:
    """Set up test data for multiple models.
    
    Note: This function should be used within a set_db_context fixture.
    """
    created_models = {}
    
    for model_class, data_list in models_data.items():
        created_instances = []
        for data in data_list:
            instance = await create_test_model(model_class, **data)
            created_instances.append(instance)
        created_models[model_class] = created_instances
    
    return created_models


def assert_model_attributes(model: Model, expected_attrs: Dict[str, Any]) -> None:
    """Assert that model has expected attributes."""
    for attr, value in expected_attrs.items():
        assert hasattr(model, attr), f"Model missing attribute: {attr}"
        actual_value = getattr(model, attr)
        assert actual_value == value, f"Attribute {attr}: expected {value}, got {actual_value}"


def assert_models_list(models: List[Model], expected_count: int) -> None:
    """Assert that models list has expected count."""
    assert len(models) == expected_count, f"Expected {expected_count} models, got {len(models)}"


# AsyncTestContext has been removed in favor of using set_db_context fixture
# for consistent database context management across tests


def create_mock_request(user_id: int = None, is_authenticated: bool = False) -> Any:
    """Create a mock request object for testing."""
    from unittest.mock import Mock
    
    request = Mock()
    request.user = Mock()
    request.user.id = user_id
    request.user.is_authenticated = is_authenticated
    
    return request


def create_mock_session() -> Any:
    """Create a mock database session for testing."""
    from unittest.mock import Mock, AsyncMock
    
    session = Mock()
    session.execute = AsyncMock()
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    
    return session