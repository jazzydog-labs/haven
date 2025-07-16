"""Repository interface for Record entity."""

from abc import ABC, abstractmethod
from uuid import UUID

from haven.domain.entities import Record


class RecordRepository(ABC):
    """Abstract repository interface for Record entities."""

    @abstractmethod
    async def get(self, record_id: UUID) -> Record | None:
        """
        Get a record by ID.

        Args:
            record_id: The UUID of the record to retrieve

        Returns:
            The Record if found, None otherwise
        """
        ...

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Record]:
        """
        Get all records with pagination.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of Record entities
        """
        ...

    @abstractmethod
    async def save(self, record: Record) -> Record:
        """
        Save a record (create or update).

        Args:
            record: The Record entity to save

        Returns:
            The saved Record entity
        """
        ...

    @abstractmethod
    async def delete(self, record_id: UUID) -> bool:
        """
        Delete a record by ID.

        Args:
            record_id: The UUID of the record to delete

        Returns:
            True if deleted, False if not found
        """
        ...

    @abstractmethod
    async def exists(self, record_id: UUID) -> bool:
        """
        Check if a record exists.

        Args:
            record_id: The UUID to check

        Returns:
            True if exists, False otherwise
        """
        ...

    @abstractmethod
    async def count(self) -> int:
        """
        Count total number of records.

        Returns:
            Total count of records
        """
        ...
