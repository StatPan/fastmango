# Your First FastMango Project

In the [Quick Start](./quick-start.md) guide, you created a new FastMango project and ran the development server. Now, let's take a closer look at the code and learn how to build your first API endpoint.

## Understanding the `main.py` File

When you create a new project with `fastmango new`, it generates a `main.py` file that contains the core of your application. Let's break down what's inside:

```python
from typing import List, Optional

from fastmango import MangoApp
from fastmango.models import Model
from sqlmodel import Field

# 1. Initialize the MangoApp
app = MangoApp(
    title="{{ project_name }}",
    database_url="sqlite+aiosqlite:///db.sqlite3",
)

# 2. Define a Model
class Item(Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None

# 3. Create API Endpoints
@app.get("/")
def read_root():
    return {"message": "Hello from your FastMango app!"}

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    await item.save()
    return item

@app.get("/items/", response_model=List[Item])
async def list_items():
    items = await Item.objects.all()
    return items

# 4. Database Initialization
@app.fastapi_app.on_event("startup")
async def on_startup():
    """
    Creates the database tables on application startup.
    """
    async with app.db_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
```

1.  **Initialize the `MangoApp`**: This is the central object of your FastMango application. It's where you configure your app's title, database connection, and other settings.
2.  **Define a Model**: This is where you define your application's data structure. FastMango uses SQLModel, which allows you to define your database tables using standard Python type hints.
3.  **Create API Endpoints**: These are the functions that handle incoming requests to your API. FastMango uses FastAPI's decorator-based syntax to define endpoints.
4.  **Database Initialization**: This function runs when your application starts up and creates the necessary database tables based on your models.

## Creating a New Endpoint

Let's add a new endpoint to our API that retrieves a single item by its ID. Add the following code to your `main.py` file:

```python
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = await Item.objects.get_or_404(id=item_id)
    return item
```

This code defines a new endpoint at `/items/{item_id}` that accepts an `item_id` as a path parameter. It then uses the `Item.objects.get_or_404()` method to retrieve the item from the database. If the item is not found, it will automatically return a 404 Not Found error.

## Interacting with Your API

Now that you've added the new endpoint, you can interact with it using the interactive documentation at `http://127.0.0.1:8000/docs`.

1.  **Create an item**: Use the `POST /items/` endpoint to create a new item. Click "Try it out", enter a name and description in the request body, and click "Execute".
2.  **List items**: Use the `GET /items/` endpoint to see a list of all the items you've created.
3.  **Get a single item**: Use the new `GET /items/{item_id}` endpoint to retrieve the item you just created. Enter the item's ID (which should be `1`) in the `item_id` field and click "Execute".

## Next Steps

You've now learned the basics of creating models and API endpoints in FastMango. From here, you can start building out your application's features. Here are some things you might want to try next:

-   Add more fields to your `Item` model.
-   Create new models for other parts of your application.
-   Explore the different types of API endpoints you can create (e.g., `PUT`, `PATCH`, `DELETE`).
-   Read the [Guides](../guides/web-apis.md) to learn about more advanced topics like authentication, permissions, and more.
