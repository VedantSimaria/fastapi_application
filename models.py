from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime

class User(Document):
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"
