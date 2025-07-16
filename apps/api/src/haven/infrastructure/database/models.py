"""SQLAlchemy models for database persistence."""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    type_annotation_map = {
        UUID: PostgresUUID(as_uuid=True),
        dict[str, Any]: JSON,
    }


class RecordModel(Base):
    """SQLAlchemy model for Record entity."""

    __tablename__ = "records"

    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of RecordModel."""
        return f"<RecordModel(id={self.id}, created_at={self.created_at})>"