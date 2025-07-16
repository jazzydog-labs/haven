"""Factory functions for database components."""

from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from haven.domain.unit_of_work import UnitOfWork
from haven.infrastructure.database.session import create_engine, create_session_factory
from haven.infrastructure.database.unit_of_work import SQLAlchemyUnitOfWork


class DatabaseFactory:
    """Factory for database components."""

    def __init__(self) -> None:
        """Initialize database factory."""
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
    
    def _ensure_initialized(self) -> None:
        """Ensure the factory is initialized."""
        if self._engine is None:
            self._engine = create_engine()
            self._session_factory = create_session_factory(self._engine)

    async def get_unit_of_work(self) -> AsyncGenerator[UnitOfWork, None]:
        """
        Get unit of work instance.
        
        Yields:
            UnitOfWork instance for the current request
        """
        self._ensure_initialized()
        assert self._session_factory is not None
        async with self._session_factory() as session:
            async with SQLAlchemyUnitOfWork(session) as uow:
                yield uow

    async def dispose(self) -> None:
        """Dispose of database connections."""
        if self._engine is not None:
            await self._engine.dispose()


# Global factory instance
db_factory = DatabaseFactory()