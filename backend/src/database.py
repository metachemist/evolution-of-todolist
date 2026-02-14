from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
import os


# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_dev")

# Create async engine
async_engine = create_async_engine(DATABASE_URL)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that provides database sessions.
    """
    async with AsyncSessionLocal() as session:
        yield session