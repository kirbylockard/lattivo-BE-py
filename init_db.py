# init_db.py
import asyncio

from app.core.database import engine, Base  # Base must be the same one your models inherit from
from app.models import habit  # noqa: F401  ensures models are registered with Base.metadata


async def main():
    # Drop all tables (probably unnecessary on a brand-new DB, but safe + explicit)
    async with engine.begin() as conn:
        print("Dropping existing tables (if any)...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating tables from models...")
        await conn.run_sync(Base.metadata.create_all)
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
