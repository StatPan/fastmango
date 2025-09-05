# fastmango Architecture Design

## 🏗️ Core Design Philosophy

fastmango reimplements **Django's proven structure and conventions** on top of **FastAPI's modern performance**, providing a framework optimized for API-centric development.

### Design Principles
- **Django Convention Inheritance**: Familiar structure for existing Django developers
- **API-First Design**: Optimized for JSON APIs rather than HTML rendering
- **Type Safety**: Complete type support through Pydantic and SQLModel
- **Async Native**: Built from the ground up with async/await design

## 📁 Project Structure

### Django vs fastmango Structure Comparison

```python
# Django Traditional Structure
myproject/
├── myproject/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── myapp/             # Django app
│   ├── models.py       # Database models
│   ├── views.py        # View functions/classes
│   ├── forms.py        # Form definitions
│   ├── urls.py         # URL routing
│   ├── admin.py        # Admin registration
│   └── apps.py         # App configuration
├── templates/         # HTML templates
├── static/           # Static files
└── manage.py         # CLI tool

# fastmango API Structure  
myproject/
├── myproject/          # Project settings
│   ├── settings.py     # App configuration (Django style)
│   ├── routes.py       # Main routing
│   ├── main.py         # FastAPI app instance
│   └── asgi.py         # ASGI server configuration
├── myapp/             # fastmango app
│   ├── models.py       # SQLModel models
│   ├── api.py          # API endpoints (views.py → api.py)
│   ├── schemas.py      # Pydantic schemas (forms.py → schemas.py)
│   ├── routes.py       # URL routing (same as urls.py)
│   ├── admin.py        # Admin registration (Django style)
│   └── apps.py         # App configuration
├── migrations/        # Alembic migrations
├── tests/            # Test files
└── fastmango.py         # CLI tool (manage.py → fastmango.py)
```

### File Naming Rationale

| Django | fastmango | Reason for Change |
|--------|--------|-------------------|
| `views.py` | `api.py` | Clearly expresses that these are API endpoints |
| `forms.py` | `schemas.py` | Pydantic schema-based data validation |
| `urls.py` | `routes.py` | Consistency with FastAPI routers |
| `manage.py` | `fastmango.py` | Framework branding and differentiation |

## 🏛️ Core Component Architecture

### 1. Model Layer (SQLModel + Django Conventions)

```python
# myapp/models.py
from fastmango import Model, Manager
from sqlmodel import Field
from datetime import datetime
from typing import Optional

class User(Model, table=True):
    """User model - Django style + SQLModel type safety"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(max_length=150, unique=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Django style Manager
    objects = Manager()
    
    class Meta:
        table_name = "users"
        
    def __str__(self):
        return f"User({self.username})"
        
    @classmethod
    async def get_active_users(cls):
        return await cls.objects.filter(is_active=True).all()
```

### 2. API Layer (FastAPI Router + Django Patterns)

```python
# myapp/api.py
from fastmango import APIRouter, Depends
from fastmango.auth import get_current_user
from .models import User
from .schemas import UserCreate, UserResponse, UserUpdate
from typing import List

api = APIRouter(prefix="/api/v1/users", tags=["users"])

@api.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100):
    """User list retrieval - Django ListView style"""
    users = await User.objects.offset(skip).limit(limit).all()
    return users

@api.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate):
    """User creation - Django CreateView style"""
    user = await User.objects.create(**user_data.dict())
    return user

@api.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """User detail retrieval - Django DetailView style"""
    user = await User.objects.get_or_404(id=user_id)
    return user

@api.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """User information update - Django UpdateView style"""
    user = await User.objects.get_or_404(id=user_id)
    updated_user = await user.update(**user_data.dict(exclude_unset=True))
    return updated_user

@api.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    """User deletion - Django DeleteView style"""
    user = await User.objects.get_or_404(id=user_id)
    await user.delete()
```

### 3. Schema Layer (Pydantic Models)

```python
# myapp/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Common user fields"""
    email: EmailStr
    username: str = Field(min_length=3, max_length=150)

class UserCreate(UserBase):
    """User creation schema - Django Form style"""
    password: str = Field(min_length=8)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "testuser",
                "password": "securepassword"
            }
        }

class UserUpdate(BaseModel):
    """User update schema - optional fields"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """User response schema - excluding sensitive information"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### 4. Routing Layer (FastAPI Router Composition)

```python
# myapp/routes.py
from .api import api as user_api

# App-level router definition (Django urls.py style)
urlpatterns = [
    user_api,  # Register to /api/v1/users path
]
```

```python
# myproject/routes.py
from fastmango import FastAPI
from myapp.routes import urlpatterns as myapp_urls

app = FastAPI(title="My Project API", version="1.0.0")

# Similar to Django's include() pattern
for router in myapp_urls:
    app.include_router(router)
```

### 5. Configuration Layer (Django-style Settings)

```python
# myproject/settings.py
import os
from typing import Optional

class Settings:
    """Django style settings"""
    
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://localhost/myproject"
    )
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React
        "http://localhost:5173",  # Vite
        "http://localhost:4173",  # Vite preview
    ]
    
    # Email settings (Django style)
    EMAIL_BACKEND: str = "smtp"
    EMAIL_HOST: Optional[str] = os.getenv("EMAIL_HOST")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS: bool = True
    
    # Media file settings
    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media/"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"

settings = Settings()
```

## 🔧 Django Convention Implementation

### 1. ORM Manager Pattern

```python
# Django style Manager implementation
class Manager:
    def __init__(self, model_class):
        self.model_class = model_class
    
    async def all(self):
        # Wrap SQLModel queries in Django style
        return await self.model_class.select()
    
    async def filter(self, **kwargs):
        # Django style filtering
        return await self.model_class.select().where(**kwargs)
    
    async def get(self, **kwargs):
        return await self.model_class.select().where(**kwargs).first()
    
    async def get_or_404(self, **kwargs):
        obj = await self.get(**kwargs)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj
    
    async def create(self, **kwargs):
        instance = self.model_class(**kwargs)
        return await instance.save()
```

### 2. Admin System (Django Admin Style)

```python
# myapp/admin.py
from fastmango.admin import admin, ModelAdmin

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    # Automatically generates /admin/users/ CRUD API
```

### 3. App System (Django Apps Pattern)

```python
# myapp/apps.py
from fastmango.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'myapp'
    verbose_name = 'My Application'
    
    def ready(self):
        # Code to execute during app initialization
        from . import signals  # Signal registration
```

## 🚀 Technology Stack Integration

### Core Technology Stack
- **FastAPI**: Async web framework
- **SQLModel**: Type-safe ORM (SQLAlchemy 2.0 + Pydantic)
- **Alembic**: Database migrations
- **Pydantic**: Data validation and serialization
- **JWT**: Authentication tokens
- **pytest**: Testing framework

### AI Integration (Optional)
- **Pydantic AI**: LLM integration and tool system
- **Type-Safe AI**: Pydantic schema-based AI function calls

## 📊 Performance and Scalability Considerations

### Async Processing
```python
# All database operations are async
async def get_user_posts(user_id: int):
    user = await User.objects.get(id=user_id)
    posts = await Post.objects.filter(author_id=user.id).all()
    return posts
```

### Connection Pooling
```python
# SQLModel + asyncpg automatic connection pool management
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
```

### Caching Support
```python
# Redis caching integration
from fastmango.cache import cache

@cache.cached(timeout=300)  # 5-minute cache
async def get_popular_posts():
    return await Post.objects.filter(views__gte=1000).all()
```

## 🔄 Migration from Django to fastmango

### Step-by-Step Migration Guide

1. **Model Conversion**: Django Model → SQLModel
2. **View Conversion**: Django View → FastAPI Router
3. **Form Conversion**: Django Form → Pydantic Schema
4. **URL Conversion**: Django urls.py → FastAPI Router
5. **Settings Conversion**: Django settings → fastmango settings

### Automatic Conversion Tool (Future Development)
```bash
fastmango migrate-from-django /path/to/django/project
```

Through this architecture, Django developers can enjoy FastAPI's modern performance using familiar patterns.