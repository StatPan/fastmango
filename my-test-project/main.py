from typing import List, Optional

from fastmango import MangoApp
from fastmango.models import Model
from sqlmodel import Field

app = MangoApp(
    title="my-test-project",
    database_url="sqlite+aiosqlite:///db.sqlite3",
)

class Item(Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None

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

@app.fastapi_app.on_event("startup")
async def on_startup():
    """
    Creates the database tables on application startup.
    """
    async with app.db_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)