# app/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./scooters.db")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
