import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

# 🔹 Load variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def main():
    print("Using DATABASE_URL:", DATABASE_URL)
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL is not set")
        return

    engine = create_async_engine(DATABASE_URL, echo=True)

    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            print("DB result:", result.scalar())
    except Exception as e:
        print("Error connecting:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
