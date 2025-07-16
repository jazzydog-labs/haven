"""Unit of Work interface."""

from abc import ABC, abstractmethod
from types import TracebackType

from haven.domain.repositories import RecordRepository


class UnitOfWork(ABC):
    """Abstract Unit of Work interface."""

    records: RecordRepository

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        """Enter the unit of work context."""
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the unit of work context."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        ...
