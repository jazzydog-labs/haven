"""Application service for Record operations."""

from typing import Any
from uuid import UUID

from haven.domain.entities import Record
from haven.domain.exceptions import RecordNotFoundError
from haven.domain.unit_of_work import UnitOfWork


class RecordService:
    """Service for managing Record entities."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        """
        Initialize service with unit of work.

        Args:
            unit_of_work: Unit of work for transaction management
        """
        self._uow = unit_of_work

    async def create_record(self, data: dict[str, Any]) -> Record:
        """
        Create a new record.

        Args:
            data: The data for the new record

        Returns:
            The created Record entity
        """
        record = Record(data=data)
        async with self._uow:
            saved_record = await self._uow.records.save(record)
            await self._uow.commit()
        return saved_record

    async def get_record(self, record_id: UUID) -> Record:
        """
        Get a record by ID.

        Args:
            record_id: The UUID of the record

        Returns:
            The Record entity

        Raises:
            RecordNotFoundError: If record doesn't exist
        """
        async with self._uow:
            record = await self._uow.records.get(record_id)
            if record is None:
                raise RecordNotFoundError(str(record_id))
            return record

    async def list_records(self, limit: int = 100, offset: int = 0) -> tuple[list[Record], int]:
        """
        List records with pagination.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            Tuple of (records list, total count)
        """
        async with self._uow:
            records = await self._uow.records.get_all(limit=limit, offset=offset)
            total = await self._uow.records.count()
            return records, total

    async def update_record(self, record_id: UUID, data: dict[str, Any]) -> Record:
        """
        Update a record's data.

        Args:
            record_id: The UUID of the record to update
            data: The new data for the record

        Returns:
            The updated Record entity

        Raises:
            RecordNotFoundError: If record doesn't exist
        """
        async with self._uow:
            record = await self._uow.records.get(record_id)
            if record is None:
                raise RecordNotFoundError(str(record_id))

            record.update_data(data)
            updated_record = await self._uow.records.save(record)
            await self._uow.commit()
            return updated_record

    async def partial_update_record(self, record_id: UUID, partial_data: dict[str, Any]) -> Record:
        """
        Partially update a record's data.

        Args:
            record_id: The UUID of the record to update
            partial_data: The partial data to merge

        Returns:
            The updated Record entity

        Raises:
            RecordNotFoundError: If record doesn't exist
        """
        async with self._uow:
            record = await self._uow.records.get(record_id)
            if record is None:
                raise RecordNotFoundError(str(record_id))

            record.merge_data(partial_data)
            updated_record = await self._uow.records.save(record)
            await self._uow.commit()
            return updated_record

    async def delete_record(self, record_id: UUID) -> bool:
        """
        Delete a record.

        Args:
            record_id: The UUID of the record to delete

        Returns:
            True if deleted, False if not found
        """
        async with self._uow:
            deleted = await self._uow.records.delete(record_id)
            if deleted:
                await self._uow.commit()
            return deleted

    async def record_exists(self, record_id: UUID) -> bool:
        """
        Check if a record exists.

        Args:
            record_id: The UUID to check

        Returns:
            True if exists, False otherwise
        """
        async with self._uow:
            return await self._uow.records.exists(record_id)
