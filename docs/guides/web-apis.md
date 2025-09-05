# Guide: Building Web APIs

This guide covers the essentials of building web APIs with FastMango, from creating your main application instance to organizing your code with routers.

## The `MangoApp` Instance

The `MangoApp` class is the heart of your FastMango application. It's a wrapper around the standard `FastAPI` class that provides additional integrations for databases, AI models, and more.

You create an instance of `MangoApp` in your `main.py` file:

```python
from fastmango import MangoApp

app = MangoApp(
    title="My Awesome API",
    version="1.0.0",
    database_url="sqlite+aiosqlite:///db.sqlite3",
)
```

The `MangoApp` constructor accepts any arguments that the standard `FastAPI` constructor does, such as `title`, `version`, and `description`. It also accepts additional arguments for configuring the database and other FastMango-specific features.

## Creating Endpoints

You can create API endpoints using decorators, just like in FastAPI. `MangoApp` provides decorators for all the standard HTTP methods:

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`
- `@app.patch()`

Here's an example of a simple `GET` endpoint:

```python
@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
```

### Path and Query Parameters

You can define path parameters using curly braces in the path string, and query parameters as arguments to your endpoint function:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

In this example, `item_id` is a path parameter, and `q` is an optional query parameter.

## Using Pydantic Schemas

FastMango uses Pydantic models (which we call "schemas") for request and response validation. This ensures that the data your API receives and sends is in the correct format.

Here's an example of how to use schemas to create a new item in the database:

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

@app.post("/items/", response_model=ItemResponse)
async def create_item(item_data: ItemCreate):
    # In a real application, you would save the item to the database here.
    # For this example, we'll just return a dummy response.
    new_item = {"id": 1, **item_data.dict()}
    return new_item
```

In this example:

- `ItemCreate` is the schema for the request body. FastMango will automatically validate the incoming data against this schema.
- `ItemResponse` is the schema for the response body. FastMango will use this schema to serialize the data you return from your endpoint.
- The `response_model` argument to the `@app.post` decorator tells FastMango to use the `ItemResponse` schema for the response.

## Organizing Your Code with `APIRouter`

As your application grows, you'll want to organize your endpoints into separate files. You can do this using `APIRouter`.

An `APIRouter` is like a mini-`MangoApp` that you can use to group related endpoints together. You can then include the router in your main `MangoApp` instance.

Here's an example of how you might structure your code:

**`myapp/api.py`**:

```python
from fastmango import APIRouter
from .schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse)
async def create_item(item_data: ItemCreate):
    # ...
```

**`main.py`**:

```python
from fastmango import MangoApp
from myapp.api import router as items_router

app = MangoApp()

app.include_router(items_router)
```

In this example, we've moved our item-related endpoints to a separate file, `myapp/api.py`, and created an `APIRouter` to group them. We've also added a `prefix` and `tags` to the router, which will be applied to all the endpoints it contains.

Finally, we've included the router in our main `MangoApp` instance using `app.include_router()`. This makes the endpoints defined in the router available under the `/items` path.

## Next Steps

You've now learned the basics of building web APIs with FastMango. To learn more, you can read the official [FastAPI documentation](https://fastapi.tiangolo.com/), as most of the concepts are the same. You can also explore the other guides in this section to learn about more advanced topics.
