
"""
Simple test app for admin functionality testing.
"""

from fastmango import MangoApp
from fastmango.models import Model
from sqlmodel import Field

class TestUser(Model, table=True):
    __tablename__ = "test_users"
    
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)

class TestPost(Model, table=True):
    __tablename__ = "test_posts"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int | None = Field(default=None, foreign_key="test_users.id")

# Create app with admin
app = MangoApp(
    title="Admin Test App",
    database_url="sqlite+aiosqlite:///test_data/admin_test.db",
    enable_admin=True,
    admin_url="/admin"
)

@app.get("/")
async def root():
    return {"message": "Admin Test App"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app.fastapi_app, host="127.0.0.1", port=8000)
