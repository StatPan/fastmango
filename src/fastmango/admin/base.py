"""
FastMango Admin - Django-style admin interface for FastMango applications.

This module provides automatic admin interface generation for FastMango models
with minimal configuration required, similar to Django's admin system.
"""

from typing import Type, List, Optional, Dict, Any
import inspect
from sqladmin import Admin, ModelView
from sqlmodel import SQLModel
from fastapi import FastAPI

from ..models import Model
from ..app import MangoApp


class FastMangoAdmin:
    """
    Django-style admin interface for FastMango applications.
    
    Automatically registers FastMango models and provides admin interface
    with minimal configuration required.
    
    Usage:
        app = MangoApp()
        admin = FastMangoAdmin()
        admin.init_app(app)
        # Models are automatically registered!
    """
    
    def __init__(self):
        """
        Initialize FastMangoAdmin.
        """
        self.app = None
        self.admin_url = None
        self._registered_models: Dict[Type[Model], ModelView] = {}
        self._custom_admins: Dict[Type[Model], Type[ModelView]] = {}
        self._models_to_register: List[Type[Model]] = []

    def init_app(self, app: MangoApp, admin_url: str = "/admin"):
        """
        Initialize the admin interface for the given app.

        Args:
            app: The MangoApp instance
            admin_url: URL path for admin interface (default: "/admin")
        """
        self.app = app
        self.admin_url = admin_url

        # Initialize SQLAdmin
        app_title = getattr(app.fastapi_app, 'title', 'FastMango')
        self.admin_app = Admin(
            app.fastapi_app,
            engine=app.db_engine,
            base_url=admin_url,
            title=f"{app_title} Admin",
            logo_url="/static/admin/logo.png"
        )
        
        # Store reference to the admin app for mounting
        self._asgi_app = self.admin_app
        
        # Auto-register all FastMango models
        self.auto_register_models()

        # Register any models that were added before init_app was called
        for model_class in self._models_to_register:
            self.register_model(model_class)

    def auto_register_models(self) -> None:
        """
        Automatically register all FastMango models found in the application.
        
        This method scans for all classes that inherit from FastMango's Model
        class and automatically registers them with the admin interface.
        """
        # Get all FastMango models from the current application
        fastmango_models = self._discover_fastmango_models()
        
        for model_class in fastmango_models:
            if self._should_register_model(model_class):
                self.register_model(model_class)
    
    def _discover_fastmango_models(self) -> List[Type[Model]]:
        """
        Discover all FastMango models in the application.
        
        Returns:
            List of FastMango model classes
        """
        models = []
        
        # Get all modules that might contain models
        # For now, we'll focus on the models module itself
        # In a more sophisticated implementation, we could scan all imported modules
        
        # Check the models module for FastMango models
        try:
            from .. import models as models_module
            for name, obj in inspect.getmembers(models_module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, Model) and 
                    obj is not Model and
                    hasattr(obj, '__tablename__')):  # Only register table models
                    models.append(obj)
        except ImportError:
            pass
        
        return models
    
    def _should_register_model(self, model_class: Type[Model]) -> bool:
        """
        Determine if a model should be registered with the admin.
        
        Args:
            model_class: The model class to check
            
        Returns:
            True if the model should be registered, False otherwise
        """
        # Don't register abstract models
        if not hasattr(model_class, '__tablename__') or not model_class.__tablename__:
            return False
        
        # Don't register if user has explicitly excluded it
        if hasattr(model_class, 'Meta') and hasattr(model_class.Meta, 'admin_exclude'):
            if model_class.Meta.admin_exclude:
                return False
        
        return True
    
    def register_model(self, model_class: Type[Model], admin_class: Optional[Type[ModelView]] = None) -> Optional[ModelView]:
        """
        Register a model with the admin interface.
        
        Args:
            model_class: The FastMango model class to register
            admin_class: Optional custom admin class
            
        Returns:
            The created ModelView instance
        """
        if not self.app:
            self._models_to_register.append(model_class)
            return None

        if model_class in self._registered_models:
            return self._registered_models[model_class]
        
        # Use custom admin class if provided, otherwise create default
        if admin_class:
            # Create instance of custom admin class
            admin_view_class = admin_class
            admin_view = admin_view_class()
        else:
            admin_view_class = self._create_default_admin_view_class(model_class)
            admin_view = admin_view_class()
        
        # Register with SQLAdmin
        self.admin_app.add_view(admin_view_class)
        
        # Track registration
        self._registered_models[model_class] = admin_view
        
        return admin_view
    
    def _create_default_admin_view_class(self, model_class: Type[Model]) -> Type[ModelView]:
        """
        Create a default admin view class for a model.
        
        Args:
            model_class: The model class to create view for
            
        Returns:
            ModelView class
        """
        # Create a dynamic ModelView class
        class_name = f"{model_class.__name__}Admin"
        
        # Determine which columns to display
        column_list = self._get_model_columns(model_class)
        search_fields = self._get_search_fields(model_class)
        
        # Get primary key information dynamically
        pk_columns = list(model_class.__table__.primary_key.columns)
        pk_column_names = [col.name for col in pk_columns]
        # Use model name for identity, not primary key field name
        identity = model_class.__tablename__
        
        # Create the admin view class with proper SQLAdmin configuration
        admin_view_class = type(
            class_name,
            (ModelView,),
            {
                "column_list": column_list,
                "column_searchable_list": search_fields,
                "form_columns": column_list,
                "name_plural": model_class.__name__ + "s",
                "name": model_class.__name__,
                # SQLAdmin requires the model to be set as a class attribute
                "model": model_class,
                # Add required SQLAdmin attributes
                "identity": identity,  # Primary key field name
                "pk_columns": pk_columns,  # Primary key columns (as column objects)
                "pk_column_names": pk_column_names,  # Primary key column names
                # Additional required attributes for SQLAdmin
                "column_details_list": column_list,
                "column_export_list": column_list,
            }
        )
        
        return admin_view_class
    
    def _create_default_admin_view(self, model_class: Type[Model]) -> ModelView:
        """
        Create a default admin view instance for a model.
        
        Args:
            model_class: The model class to create view for
            
        Returns:
            ModelView instance
        """
        admin_view_class = self._create_default_admin_view_class(model_class)
        return admin_view_class()
    
    def _get_model_columns(self, model_class: Type[Model]) -> List[str]:
        """
        Get the list of columns to display in admin for a model.
        
        Args:
            model_class: The model class
            
        Returns:
            List of column names
        """
        # Get all field names from the model
        columns = []
        
        for field_name, field_info in model_class.model_fields.items():
            # Skip sensitive fields like passwords
            if 'password' in field_name.lower():
                continue
            
            # Include foreign key fields for simplicity in default view
            # This ensures all fields are included in the form
            
            columns.append(field_name)
        
        # Ensure we have some columns
        if not columns:
            columns = ['id']
        
        return columns
    
    def _get_search_fields(self, model_class: Type[Model]) -> List[str]:
        """
        Get the list of fields that should be searchable.
        
        Args:
            model_class: The model class
            
        Returns:
            List of searchable field names
        """
        search_fields = []
        
        from typing import get_origin, get_args, Union
        
        for field_name, field_info in model_class.model_fields.items():
            # Include string fields in search
            if field_info.annotation:
                # Check if it's a string type (including Optional[str])
                annotation = field_info.annotation
                origin = get_origin(annotation)
                args = get_args(annotation)
                
                is_string_type = (
                    annotation is str or
                    (origin is Union and str in args) or
                    (origin is Union and len(args) == 2 and args[0] is str and args[1] is type(None))
                )
                
                if is_string_type or \
                   'email' in field_name.lower() or \
                   'name' in field_name.lower() or \
                   'username' in field_name.lower():
                    search_fields.append(field_name)
        
        return search_fields
    
    def register_custom_admin(self, model_class: Type[Model], admin_class: Type[ModelView]) -> None:
        """
        Register a custom admin class for a model.
        
        Args:
            model_class: The model class
            admin_class: The custom admin class
        """
        self._custom_admins[model_class] = admin_class
        self.register_model(model_class, admin_class)
    
    def get_registered_models(self) -> List[Type[Model]]:
        """
        Get list of registered models.
        
        Returns:
            List of registered model classes
        """
        return list(self._registered_models.keys())
    
    def is_model_registered(self, model_class: Type[Model]) -> bool:
        """
        Check if a model is registered with the admin.
        
        Args:
            model_class: The model class to check
            
        Returns:
            True if registered, False otherwise
        """
        return model_class in self._registered_models
    
    def setup_admin_routes(self) -> None:
        """
        Setup admin routes and ensure proper integration.
        
        This method is called automatically during initialization but
        can be called manually if needed.
        """
        # SQLAdmin automatically sets up routes during initialization
        # This method is for future extensibility
        pass
    
    @property
    def asgi_app(self):
        """
        Get the ASGI application for mounting.
        
        Returns:
            The ASGI application that can be mounted to FastAPI
        """
        return self._asgi_app