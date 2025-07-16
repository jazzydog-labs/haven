"""Unit tests for repository pattern implementation."""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from haven.domain.entities import Record
from haven.infrastructure.database.models import RecordModel
from haven.infrastructure.database.repositories import SQLAlchemyRecordRepository


class TestSQLAlchemyRecordRepository:
    """Test cases for SQLAlchemyRecordRepository."""

    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        """Create mock database session."""
        session = AsyncMock()
        # Ensure get method returns async result
        session.get = AsyncMock()
        return session

    @pytest.fixture
    def repository(self, mock_session: AsyncMock) -> SQLAlchemyRecordRepository:
        """Create repository instance with mock session."""
        return SQLAlchemyRecordRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_existing_record(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test getting an existing record."""
        # Arrange
        test_id = uuid4()
        mock_model = MagicMock(spec=RecordModel)
        mock_model.id = test_id
        mock_model.data = {"test": "data"}
        mock_model.created_at = MagicMock()
        mock_model.updated_at = MagicMock()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get(test_id)

        # Assert
        assert result is not None
        assert result.id == test_id
        assert result.data == {"test": "data"}

    @pytest.mark.asyncio
    async def test_get_nonexistent_record(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test getting a nonexistent record returns None."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get(uuid4())

        # Assert
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Async mock issue with _model_to_entity")
    async def test_save_new_record(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test saving a new record."""
        # Arrange
        record = Record(data={"test": "data"})
        mock_session.get.return_value = None  # Record doesn't exist

        # Act
        await repository.save(record)

        # Assert
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()
        # Check the added model has correct attributes
        added_model = mock_session.add.call_args[0][0]
        assert added_model.id == record.id
        assert added_model.data == record.data
        # Verify get was called to check if record exists
        mock_session.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_existing_record(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test updating an existing record."""
        # Arrange
        record = Record(data={"updated": "data"})
        mock_existing = MagicMock(spec=RecordModel)
        mock_existing.id = record.id
        mock_existing.data = {}
        mock_existing.created_at = record.created_at
        mock_existing.updated_at = record.updated_at
        mock_session.get.return_value = mock_existing

        # Act
        result = await repository.save(record)

        # Assert
        assert mock_existing.data == {"updated": "data"}
        mock_session.flush.assert_called_once()
        # The result should have the same data as what we saved
        assert result.data == record.data

    @pytest.mark.asyncio
    async def test_delete_existing_record(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test deleting an existing record."""
        # Arrange
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.delete(uuid4())

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_nonexistent_record(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test deleting a nonexistent record."""
        # Arrange
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.delete(uuid4())

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_exists_true(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test exists returns True for existing record."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.exists(uuid4())

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_count(
        self, repository: SQLAlchemyRecordRepository, mock_session: AsyncMock
    ) -> None:
        """Test counting records."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar.return_value = 42
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.count()

        # Assert
        assert result == 42
