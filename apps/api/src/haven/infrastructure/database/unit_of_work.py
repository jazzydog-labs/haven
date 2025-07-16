"""SQLAlchemy implementation of Unit of Work pattern."""

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from haven.domain.unit_of_work import UnitOfWork
from haven.infrastructure.database.repositories import SQLAlchemyRecordRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy implementation of Unit of Work pattern."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize unit of work with database session.

        Args:
            session: AsyncSession for database operations
        """
        self._session = session
        self._transaction: AsyncSessionTransaction | None = None

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        """Enter the unit of work context."""
        # Check if a transaction is already active
        if not self._session.in_transaction():
            self._transaction = await self._session.begin()
        self.records = SQLAlchemyRecordRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the unit of work context."""
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        """Commit the current transaction."""
        if self._transaction:
            await self._transaction.commit()
            self._transaction = None

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        if self._transaction:
            await self._transaction.rollback()
            self._transaction = None
