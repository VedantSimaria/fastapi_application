from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    mongodb_url: str

    class Config:
        env_file = ".env"

class UserCreate(BaseModel):
    username: str
    email: str

app = FastAPI()
settings = Settings()

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client.get_default_database()
    await init_beanie(database, document_models=[User])
    logger.info("Connected to MongoDB")

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    new_user = User(username=user.username, email=user.email)
    await new_user.insert()
    logger.info(f"Created user: {new_user}")
    return new_user

@app.get("/users", response_model=list[User])
async def get_users():
    users = await User.find_all().to_list()
    logger.info(f"Retrieved users: {users}")
    return users
