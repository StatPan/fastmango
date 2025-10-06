"""
FastMango Admin Views - Base classes for custom admin interfaces.

This module provides base classes that users can extend to create
custom admin interfaces for their FastMango models.
"""

from typing import Any, Dict, List, Optional, Type
from sqladmin import ModelView
from sqlmodel import SQLModel

from ..models import Model


class ModelAdmin(ModelView):
    """
    Base class for custom FastMango admin views.
    
    Users can extend this class to create custom admin interfaces
    for their FastMango models, similar to Django's ModelAdmin.
    
    Example:
        class UserAdmin(ModelAdmin):
            list_display = ['username', 'email', 'is_active']
            list_filter = ['is_active', 'created_at']
            search_fields = ['username', 'email']
            
        admin.register_custom_admin(User, UserAdmin)
    """
    
    # Django-like admin configuration options
    list_display: List[str] = []
    list_filter: List[str] = []
    search_fields: List[str] = []
    list_per_page: int = 25
    ordering: List[str] = []
    readonly_fields: List[str] = []
    exclude: List[str] = []
    fields: Optional[List[str]] = None
    fieldsets: Optional[List[Dict[str, Any]]] = None
    
    def __init__(self, model: Type[Model], **kwargs):
        """
        Initialize the ModelAdmin.
        
        Args:
            model: The FastMango model class
            **kwargs: Additional arguments passed to SQLAdmin's ModelView
        """
        # Apply Django-like configurations to SQLAdmin ModelView
        self._apply_django_configurations()
        
        # Set default values if not provided
        if not hasattr(self, 'name') or not self.name:
            self.name = model.__name__
        if not hasattr(self, 'name_plural') or not self.name_plural:
            self.name_plural = model.__name__ + "s"
        
        # Set model as class attribute
        self.model = model
        
        super().__init__(model=model, **kwargs)
    
    def _apply_django_configurations(self) -> None:
        """
        Apply Django-like admin configurations to SQLAdmin ModelView.
        """
        # Map Django-style configurations to SQLAdmin equivalents
        if self.list_display:
            self.column_list = self.list_display
        
        if self.search_fields:
            self.column_searchable_list = self.search_fields
        
        if self.list_filter:
            self.column_filters = self.list_filter
        
        if self.ordering:
            self.column_default_sort = self.ordering
        
        if self.readonly_fields:
            self.form_readonly_fields = self.readonly_fields
        
        if self.exclude:
            self.form_excluded_columns = self.exclude
        
        if self.fields:
            self.form_columns = self.fields
        
        # Set pagination
        if self.list_per_page:
            self.page_size = self.list_per_page
    
    def get_list_display(self, request: Any) -> List[str]:
        """
        Get the list of fields to display in the list view.
        
        Args:
            request: The request object
            
        Returns:
            List of field names
        """
        return self.list_display or self._get_default_list_display()
    
    def _get_default_list_display(self) -> List[str]:
        """
        Get default list display fields if not specified.
        
        Returns:
            List of default field names
        """
        # Try to use common fields
        common_fields = ['username', 'name', 'title', 'email']
        model_fields = list(self.model.model_fields.keys())
        
        # Find first available common field
        for field in common_fields:
            if field in model_fields:
                return [field, 'id']
        
        # Fall back to id and first string field
        for field in model_fields:
            if 'str' in str(self.model.model_fields[field].annotation):
                return [field, 'id']
        
        return ['id']
    
    def get_search_fields(self, request: Any) -> List[str]:
        """
        Get the list of searchable fields.
        
        Args:
            request: The request object
            
        Returns:
            List of searchable field names
        """
        return self.search_fields or self._get_default_search_fields()
    
    def _get_default_search_fields(self) -> List[str]:
        """
        Get default searchable fields if not specified.
        
        Returns:
            List of default searchable field names
        """
        search_fields = []
        model_fields = self.model.model_fields
        
        for field_name, field_info in model_fields.items():
            # Include string fields
            if 'str' in str(field_info.annotation):
                search_fields.append(field_name)
        
        return search_fields
    
    def get_list_filter(self, request: Any) -> List[str]:
        """
        Get the list of filter fields.
        
        Args:
            request: The request object
            
        Returns:
            List of filter field names
        """
        return self.list_filter or self._get_default_list_filter()
    
    def _get_default_list_filter(self) -> List[str]:
        """
        Get default filter fields if not specified.
        
        Returns:
            List of default filter field names
        """
        filter_fields = []
        model_fields = self.model.model_fields
        
        for field_name, field_info in model_fields.items():
            # Include boolean and datetime fields for filtering
            field_type = str(field_info.annotation)
            if ('bool' in field_type or 
                'datetime' in field_type or 
                'date' in field_type):
                filter_fields.append(field_name)
        
        return filter_fields
    
    def get_readonly_fields(self, request: Any, obj: Optional[SQLModel] = None) -> List[str]:
        """
        Get readonly fields for the form.
        
        Args:
            request: The request object
            obj: The object being edited (if any)
            
        Returns:
            List of readonly field names
        """
        return self.readonly_fields or []
    
    def get_exclude(self, request: Any) -> List[str]:
        """
        Get fields to exclude from the form.
        
        Args:
            request: The request object
            
        Returns:
            List of excluded field names
        """
        return self.exclude or []
    
    def get_fields(self, request: Any) -> Optional[List[str]]:
        """
        Get fields to include in the form.
        
        Args:
            request: The request object
            
        Returns:
            List of field names or None for all fields
        """
        return self.fields
    
    def save_model(self, request: Any, obj: SQLModel, form: Any, change: bool) -> None:
        """
        Save the model instance.
        
        Args:
            request: The request object
            obj: The model instance
            form: The form data
            change: Whether this is an update (True) or create (False)
        """
        # Use FastMango's save method if available
        if hasattr(obj, 'save'):
            import asyncio
            if asyncio.iscoroutinefunction(obj.save):
                # In a real implementation, we'd need to handle async properly
                # For now, we'll rely on SQLAdmin's default behavior
                pass
        # SQLAdmin will handle the actual saving
    
    def delete_model(self, request: Any, obj: SQLModel) -> None:
        """
        Delete the model instance.
        
        Args:
            request: The request object
            obj: The model instance to delete
        """
        # Use FastMango's delete method if available
        if hasattr(obj, 'delete'):
            import asyncio
            if asyncio.iscoroutinefunction(obj.delete):
                # In a real implementation, we'd need to handle async properly
                # For now, we'll rely on SQLAdmin's default behavior
                pass
        # SQLAdmin will handle the actual deletion


class InlineModelAdmin:
    """
    Base class for inline admin editing.
    
    This is a placeholder for future implementation of inline editing
    similar to Django's TabularInline and StackedInline.
    """
    
    model: Type[Model]
    extra: int = 3
    max_num: Optional[int] = None
    min_num: Optional[int] = None
    
    def __init__(self, parent_model: Type[Model], admin_site: Any):
        """
        Initialize the inline admin.
        
        Args:
            parent_model: The parent model class
            admin_site: The admin site instance
        """
        self.parent_model = parent_model
        self.admin_site = admin_site


class TabularInline(InlineModelAdmin):
    """
    Tabular inline editing similar to Django's TabularInline.
    """
    pass


class StackedInline(InlineModelAdmin):
    """
    Stacked inline editing similar to Django's StackedInline.
    """
    pass