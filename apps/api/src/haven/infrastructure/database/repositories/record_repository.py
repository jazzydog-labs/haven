"""SQLAlchemy implementation of RecordRepository."""

from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities import Record
from haven.domain.repositories import RecordRepository
from haven.infrastructure.database.models import RecordModel


class SQLAlchemyRecordRepository(RecordRepository):
    """SQLAlchemy implementation of RecordRepository."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize repository with database session.

        Args:
            session: AsyncSession for database operations
        """
        self._session = session

    async def get(self, record_id: UUID) -> Record | None:
        """Get a record by ID."""
        result = await self._session.execute(select(RecordModel).where(RecordModel.id == str(record_id)))
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._model_to_entity(model)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Record]:
        """Get all records with pagination."""
        result = await self._session.execute(
            select(RecordModel).order_by(RecordModel.created_at.desc()).limit(limit).offset(offset)
        )
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def save(self, record: Record) -> Record:
        """Save a record (create or update)."""
        # Check if record exists
        existing = await self._session.get(RecordModel, str(record.id))

        if existing:
            # Update existing record
            existing.data = record.data
            existing.updated_at = record.updated_at
            model = existing
        else:
            # Create new record
            model = self._entity_to_model(record)
            self._session.add(model)

        await self._session.flush()
        return self._model_to_entity(model)

    async def delete(self, record_id: UUID) -> bool:
        """Delete a record by ID."""
        result = await self._session.execute(delete(RecordModel).where(RecordModel.id == str(record_id)))
        return result.rowcount > 0

    async def exists(self, record_id: UUID) -> bool:
        """Check if a record exists."""
        result = await self._session.execute(
            select(func.count()).select_from(RecordModel).where(RecordModel.id == str(record_id))
        )
        count = result.scalar() or 0
        return count > 0

    async def count(self) -> int:
        """Count total number of records."""
        result = await self._session.execute(select(func.count()).select_from(RecordModel))
        return result.scalar() or 0

    @staticmethod
    def _model_to_entity(model: RecordModel) -> Record:
        """Convert SQLAlchemy model to domain entity."""
        return Record(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            data=model.data,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _entity_to_model(entity: Record) -> RecordModel:
        """Convert domain entity to SQLAlchemy model."""
        return RecordModel(
            id=str(entity.id),
            data=entity.data,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
