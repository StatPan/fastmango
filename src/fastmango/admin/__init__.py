from typing import Dict, Type, Any
from sqlmodel import SQLModel


class Admin:
    """FastMango Admin interface for managing models."""
    
    def __init__(self):
        self.models: Dict[str, Type[SQLModel]] = {}
    
    def register_model(self, model_class: Type[SQLModel]) -> None:
        """Register a model with the admin interface."""
        model_name = model_class.__name__
        
        if model_name in self.models:
            raise ValueError(f"Model {model_name} is already registered")
        
        self.models[model_name] = model_class
    
    def unregister_model(self, model_name: str) -> None:
        """Unregister a model from the admin interface."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} is not registered")
        
        del self.models[model_name]
    
    def get_model(self, model_name: str) -> Type[SQLModel] | None:
        """Get a registered model by name."""
        return self.models.get(model_name)