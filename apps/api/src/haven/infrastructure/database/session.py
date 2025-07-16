"""Database session management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from haven.config import get_settings


def create_engine() -> AsyncEngine:
    """Create async SQLAlchemy engine."""
    settings = get_settings()
    
    return create_async_engine(
        settings.database.dsn,
        echo=settings.app.debug,
        pool_size=settings.database.pool.size,
        max_overflow=settings.database.pool.max_overflow,
        pool_timeout=settings.database.pool.timeout,
        pool_recycle=settings.database.pool.recycle,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create async session factory."""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session context manager."""
    engine = create_engine()
    async_session = create_session_factory(engine)
    
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
    
    await engine.dispose()