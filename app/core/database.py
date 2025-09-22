# app/core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

# Load environment variables from .env
load_dotenv()

# Database URL from .env, convert to asyncpg for async connections
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql+psycopg2", "postgresql+asyncpg")

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
