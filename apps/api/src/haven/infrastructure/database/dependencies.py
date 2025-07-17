"""Database dependencies for FastAPI."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from haven.infrastructure.database.factory import db_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for FastAPI dependency injection.
    
    This provides a raw AsyncSession for use in routes that need
    direct database access without the full unit of work pattern.
    """
    factory = db_factory
    factory._ensure_initialized()
    
    assert factory._session_factory is not None
    async with factory._session_factory() as session:
        try:
            yield session
        finally:
            await session.close()