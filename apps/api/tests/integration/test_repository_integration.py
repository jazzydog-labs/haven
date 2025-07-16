"""Integration tests for repository with real database."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities import Record
from haven.infrastructure.database.repositories import SQLAlchemyRecordRepository
from tests.fixtures import sample_record, sample_records


@pytest.mark.integration
class TestRepositoryIntegration:
    """Integration tests for SQLAlchemyRecordRepository."""

    @pytest.mark.asyncio
    async def test_save_and_retrieve_record(
        self, test_session: AsyncSession, sample_record: Record
    ) -> None:
        """Test saving and retrieving a record."""
        repository = SQLAlchemyRecordRepository(test_session)
        
        # Save record
        saved = await repository.save(sample_record)
        await test_session.commit()
        
        # Retrieve record
        retrieved = await repository.get(saved.id)
        
        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.data == saved.data

    @pytest.mark.asyncio
    async def test_update_existing_record(
        self, test_session: AsyncSession, sample_record: Record
    ) -> None:
        """Test updating an existing record."""
        repository = SQLAlchemyRecordRepository(test_session)
        
        # Save initial record
        await repository.save(sample_record)
        await test_session.commit()
        
        # Update record
        sample_record.update_data({"updated": "data"})
        updated = await repository.save(sample_record)
        await test_session.commit()
        
        # Verify update
        retrieved = await repository.get(sample_record.id)
        assert retrieved is not None
        assert retrieved.data == {"updated": "data"}
        assert retrieved.updated_at > retrieved.created_at

    @pytest.mark.asyncio
    async def test_delete_record(
        self, test_session: AsyncSession, sample_record: Record
    ) -> None:
        """Test deleting a record."""
        repository = SQLAlchemyRecordRepository(test_session)
        
        # Save record
        await repository.save(sample_record)
        await test_session.commit()
        
        # Delete record
        deleted = await repository.delete(sample_record.id)
        await test_session.commit()
        
        assert deleted is True
        
        # Verify deletion
        retrieved = await repository.get(sample_record.id)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_list_records_with_pagination(
        self, test_session: AsyncSession, sample_records: list[Record]
    ) -> None:
        """Test listing records with pagination."""
        repository = SQLAlchemyRecordRepository(test_session)
        
        # Save multiple records
        for record in sample_records:
            await repository.save(record)
        await test_session.commit()
        
        # Test pagination
        page1 = await repository.get_all(limit=2, offset=0)
        page2 = await repository.get_all(limit=2, offset=2)
        
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].id != page2[0].id

    @pytest.mark.asyncio
    async def test_count_records(
        self, test_session: AsyncSession, sample_records: list[Record]
    ) -> None:
        """Test counting records."""
        repository = SQLAlchemyRecordRepository(test_session)
        
        # Initially empty
        initial_count = await repository.count()
        assert initial_count == 0
        
        # Save records
        for record in sample_records:
            await repository.save(record)
        await test_session.commit()
        
        # Count after saving
        final_count = await repository.count()
        assert final_count == len(sample_records)

    @pytest.mark.asyncio
    async def test_exists_check(
        self, test_session: AsyncSession, sample_record: Record
    ) -> None:
        """Test checking if record exists."""
        repository = SQLAlchemyRecordRepository(test_session)
        
        # Before saving
        exists_before = await repository.exists(sample_record.id)
        assert exists_before is False
        
        # Save record
        await repository.save(sample_record)
        await test_session.commit()
        
        # After saving
        exists_after = await repository.exists(sample_record.id)
        assert exists_after is True