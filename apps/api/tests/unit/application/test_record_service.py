"""Unit tests for RecordService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from haven.application.services import RecordService
from haven.domain.entities import Record
from haven.domain.exceptions import RecordNotFoundError


class TestRecordService:
    """Test cases for RecordService."""

    @pytest.fixture
    def mock_uow(self) -> AsyncMock:
        """Create mock unit of work."""
        uow = AsyncMock()
        uow.records = AsyncMock()
        uow.__aenter__.return_value = uow
        uow.__aexit__.return_value = None
        return uow

    @pytest.fixture
    def service(self, mock_uow: AsyncMock) -> RecordService:
        """Create service instance with mock unit of work."""
        return RecordService(mock_uow)

    @pytest.mark.asyncio
    async def test_create_record(self, service: RecordService, mock_uow: AsyncMock) -> None:
        """Test creating a new record."""
        # Arrange
        test_data = {"key": "value"}
        mock_record = Record(data=test_data)
        mock_uow.records.save.return_value = mock_record

        # Act
        result = await service.create_record(test_data)

        # Assert
        assert result.data == test_data
        mock_uow.records.save.assert_called_once()
        mock_uow.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_existing_record(self, service: RecordService, mock_uow: AsyncMock) -> None:
        """Test getting an existing record."""
        # Arrange
        test_id = uuid4()
        mock_record = Record(id=test_id, data={"test": "data"})
        mock_uow.records.get.return_value = mock_record

        # Act
        result = await service.get_record(test_id)

        # Assert
        assert result.id == test_id
        assert result.data == {"test": "data"}
        mock_uow.records.get.assert_called_once_with(test_id)

    @pytest.mark.asyncio
    async def test_get_nonexistent_record(
        self, service: RecordService, mock_uow: AsyncMock
    ) -> None:
        """Test getting a nonexistent record raises error."""
        # Arrange
        test_id = uuid4()
        mock_uow.records.get.return_value = None

        # Act & Assert
        with pytest.raises(RecordNotFoundError):
            await service.get_record(test_id)

    @pytest.mark.asyncio
    async def test_list_records(self, service: RecordService, mock_uow: AsyncMock) -> None:
        """Test listing records with pagination."""
        # Arrange
        mock_records = [Record(data={"id": i}) for i in range(3)]
        mock_uow.records.get_all.return_value = mock_records
        mock_uow.records.count.return_value = 42

        # Act
        records, total = await service.list_records(limit=10, offset=0)

        # Assert
        assert len(records) == 3
        assert total == 42
        mock_uow.records.get_all.assert_called_once_with(limit=10, offset=0)

    @pytest.mark.asyncio
    async def test_update_record(self, service: RecordService, mock_uow: AsyncMock) -> None:
        """Test updating a record."""
        # Arrange
        test_id = uuid4()
        original_record = Record(id=test_id, data={"old": "data"})
        new_data = {"new": "data"}
        mock_uow.records.get.return_value = original_record
        mock_uow.records.save.return_value = original_record

        # Act
        result = await service.update_record(test_id, new_data)

        # Assert
        assert result.data == new_data
        mock_uow.records.save.assert_called_once()
        mock_uow.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_nonexistent_record(
        self, service: RecordService, mock_uow: AsyncMock
    ) -> None:
        """Test updating a nonexistent record raises error."""
        # Arrange
        test_id = uuid4()
        mock_uow.records.get.return_value = None

        # Act & Assert
        with pytest.raises(RecordNotFoundError):
            await service.update_record(test_id, {"new": "data"})

    @pytest.mark.asyncio
    async def test_partial_update_record(self, service: RecordService, mock_uow: AsyncMock) -> None:
        """Test partially updating a record."""
        # Arrange
        test_id = uuid4()
        original_record = Record(id=test_id, data={"old": "data", "keep": "this"})
        partial_data = {"old": "updated"}
        mock_uow.records.get.return_value = original_record
        mock_uow.records.save.return_value = original_record

        # Act
        result = await service.partial_update_record(test_id, partial_data)

        # Assert
        assert result.data == {"old": "updated", "keep": "this"}
        mock_uow.records.save.assert_called_once()
        mock_uow.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_existing_record(
        self, service: RecordService, mock_uow: AsyncMock
    ) -> None:
        """Test deleting an existing record."""
        # Arrange
        test_id = uuid4()
        mock_uow.records.delete.return_value = True

        # Act
        result = await service.delete_record(test_id)

        # Assert
        assert result is True
        mock_uow.records.delete.assert_called_once_with(test_id)
        mock_uow.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_nonexistent_record(
        self, service: RecordService, mock_uow: AsyncMock
    ) -> None:
        """Test deleting a nonexistent record."""
        # Arrange
        test_id = uuid4()
        mock_uow.records.delete.return_value = False

        # Act
        result = await service.delete_record(test_id)

        # Assert
        assert result is False
        mock_uow.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_record_exists(self, service: RecordService, mock_uow: AsyncMock) -> None:
        """Test checking if record exists."""
        # Arrange
        test_id = uuid4()
        mock_uow.records.exists.return_value = True

        # Act
        result = await service.record_exists(test_id)

        # Assert
        assert result is True
        mock_uow.records.exists.assert_called_once_with(test_id)
