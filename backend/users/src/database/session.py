from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.settings import postgres_settings

async_engine = create_async_engine(
    postgres_settings.url,
    future=True,
    pool_size=20,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=postgres_settings.echo,
)

postgres_session_factory = async_sessionmaker(
    future=True,
    class_=AsyncSession,
    bind=async_engine,
    expire_on_commit=False,
)


async def create_postgres_session() -> AsyncIterator[AsyncSession]:
    async with postgres_session_factory() as session:
        yield session
