# app/core/database.py
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Load environment variables from .env
load_dotenv()

# Database URL from .env, convert to asyncpg for async connections
DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "postgresql+psycopg2", "postgresql+asyncpg"
)

# Create async engine and session maker
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Base class for models
class Base(DeclarativeBase):
    pass


# Dependency to provide a session for FastAPI routes
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
