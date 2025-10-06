import pytest
from sqlmodel import Field, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession

from fastmango.models import Model, Manager


class SampleTestModel(Model, table=True):
    """Test model for unit testing."""
    __tablename__ = "test_models"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_model_manager_creation():
    """Test that model manager is created correctly."""
    assert hasattr(SampleTestModel, 'objects')
    assert isinstance(SampleTestModel.objects, Manager)
    assert SampleTestModel.objects.model_class == SampleTestModel


@pytest.mark.asyncio
@pytest.mark.unit
async def test_model_creation():
    """Test basic model creation."""
    model = SampleTestModel(name="Test", description="Test description")
    
    assert model.name == "Test"
    assert model.description == "Test description"
    assert model.id is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_manager_get_session_context_error():
    """Test that manager raises error when no session is in context."""
    with pytest.raises(RuntimeError, match="Database session not available in context"):
        await SampleTestModel.objects.all()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_model_save_context_error():
    """Test that model save raises error when no session is in context."""
    model = SampleTestModel(name="Test")
    
    with pytest.raises(RuntimeError, match="Database session not available in context"):
        await model.save()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_model_delete_context_error():
    """Test that model delete raises error when no session is in context."""
    model = SampleTestModel(name="Test")
    
    with pytest.raises(RuntimeError, match="Database session not available in context"):
        await model.delete()


@pytest.mark.asyncio
@pytest.mark.database
async def test_model_crud_operations(set_db_context):
    """Test complete CRUD operations."""
    # Create
    model = await SampleTestModel.objects.create(
        name="Test Model",
        description="A test model"
    )
    
    assert model.id is not None
    assert model.name == "Test Model"
    assert model.description == "A test model"
    
    # Read all
    all_models = await SampleTestModel.objects.all()
    assert len(all_models) == 1
    assert all_models[0].id == model.id
    
    # Read by filter
    filtered_models = await SampleTestModel.objects.filter(name="Test Model")
    assert len(filtered_models) == 1
    assert filtered_models[0].id == model.id
    
    # Read single
    found_model = await SampleTestModel.objects.get(id=model.id)
    assert found_model is not None
    assert found_model.name == "Test Model"
    
    # Update
    model.name = "Updated Model"
    await model.save()
    
    updated_model = await SampleTestModel.objects.get(id=model.id)
    assert updated_model.name == "Updated Model"
    
    # Delete
    await model.delete()
    
    deleted_model = await SampleTestModel.objects.get(id=model.id)
    assert deleted_model is None