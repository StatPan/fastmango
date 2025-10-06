import asyncio
from typing import Any, Dict, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

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
    """Clear all data for a specific model."""
    all_instances = await model_class.objects.all()
    for instance in all_instances:
        await instance.delete()


async def setup_test_data(
    session: AsyncSession,
    models_data: Dict[Type[Model], List[Dict[str, Any]]]
) -> Dict[Type[Model], List[Model]]:
    """Set up test data for multiple models."""
    from fastmango.models import db_session_context
    
    # Set the database session context
    token = db_session_context.set(session)
    
    try:
        created_models = {}
        
        for model_class, data_list in models_data.items():
            created_instances = []
            for data in data_list:
                instance = await create_test_model(model_class, **data)
                created_instances.append(instance)
            created_models[model_class] = created_instances
        
        return created_models
    
    finally:
        db_session_context.reset(token)


def assert_model_attributes(model: Model, expected_attrs: Dict[str, Any]) -> None:
    """Assert that model has expected attributes."""
    for attr, value in expected_attrs.items():
        assert hasattr(model, attr), f"Model missing attribute: {attr}"
        actual_value = getattr(model, attr)
        assert actual_value == value, f"Attribute {attr}: expected {value}, got {actual_value}"


def assert_models_list(models: List[Model], expected_count: int) -> None:
    """Assert that models list has expected count."""
    assert len(models) == expected_count, f"Expected {expected_count} models, got {len(models)}"


class AsyncTestContext:
    """Context manager for async test operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.token = None
    
    async def __aenter__(self):
        from fastmango.models import db_session_context
        self.token = db_session_context.set(self.session)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        from fastmango.models import db_session_context
        if self.token:
            db_session_context.reset(self.token)


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