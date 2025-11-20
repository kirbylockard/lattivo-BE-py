# app/core/database.py
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import make_url

# Load .env when running locally (Render just uses real env vars)
load_dotenv()

raw_url = os.getenv("DATABASE_URL")
if not raw_url:
    raise RuntimeError(
        "DATABASE_URL is not set – check your environment / Render settings"
    )

# If user accidentally used a sync-style URL, upgrade it to asyncpg
# e.g. "postgresql://..." -> "postgresql+asyncpg://..."
if raw_url.startswith("postgresql://"):
    raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif raw_url.startswith("postgres://"):
    # older style from some providers
    raw_url = raw_url.replace("postgres://", "postgresql+asyncpg://", 1)

DATABASE_URL = raw_url

# Optional: small, safe log so you can see what's being used without leaking the password
url_info = make_url(DATABASE_URL)
print(
    "[database] Using DATABASE_URL:",
    f"driver={url_info.drivername}, host={url_info.host}, port={url_info.port}, "
    f"database={url_info.database}, username={url_info.username}",
    flush=True,
)

# Create async engine & session factory
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # flip to True if you want verbose SQL logs locally
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields an AsyncSession."""
    async with async_session() as session:
        yield session
