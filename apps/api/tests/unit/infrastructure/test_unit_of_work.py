"""Unit tests for Unit of Work implementation."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from haven.infrastructure.database.unit_of_work import SQLAlchemyUnitOfWork


class TestSQLAlchemyUnitOfWork:
    """Test cases for SQLAlchemyUnitOfWork."""

    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        """Create mock database session."""
        session = AsyncMock()
        transaction = AsyncMock()
        transaction.commit = AsyncMock()
        transaction.rollback = AsyncMock()
        session.begin = AsyncMock(return_value=transaction)
        session.in_transaction = MagicMock(return_value=False)
        return session

    @pytest.fixture
    def uow(self, mock_session: AsyncMock) -> SQLAlchemyUnitOfWork:
        """Create unit of work instance with mock session."""
        return SQLAlchemyUnitOfWork(mock_session)

    @pytest.mark.asyncio
    async def test_context_manager_success(self, uow: SQLAlchemyUnitOfWork) -> None:
        """Test unit of work context manager with successful transaction."""
        async with uow:
            assert hasattr(uow, "records")
            assert uow._transaction is not None

        # Verify commit was called
        assert uow._transaction is None

    @pytest.mark.asyncio
    async def test_context_manager_with_exception(self, uow: SQLAlchemyUnitOfWork) -> None:
        """Test unit of work context manager with exception."""
        with pytest.raises(ValueError):
            async with uow:
                assert hasattr(uow, "records")
                raise ValueError("Test exception")

        # Verify rollback was called
        assert uow._transaction is None

    @pytest.mark.asyncio
    async def test_explicit_commit(self, uow: SQLAlchemyUnitOfWork) -> None:
        """Test explicit commit."""
        async with uow:
            await uow.commit()
            assert uow._transaction is None

    @pytest.mark.asyncio
    async def test_explicit_rollback(self, uow: SQLAlchemyUnitOfWork) -> None:
        """Test explicit rollback."""
        async with uow:
            await uow.rollback()
            assert uow._transaction is None

    @pytest.mark.asyncio
    async def test_repository_access(self, uow: SQLAlchemyUnitOfWork) -> None:
        """Test accessing repository through unit of work."""
        async with uow:
            assert uow.records is not None
            assert hasattr(uow.records, "get")
            assert hasattr(uow.records, "save")
            assert hasattr(uow.records, "delete")
