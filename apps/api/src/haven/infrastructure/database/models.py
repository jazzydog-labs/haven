"""SQLAlchemy models for database persistence."""

from datetime import datetime
from typing import Any, ClassVar, Optional
from uuid import UUID

from sqlalchemy import JSON, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    type_annotation_map: ClassVar[dict[type, Any]] = {
        UUID: PostgresUUID(as_uuid=True),
        dict[str, Any]: JSON,
    }


__all__ = ["Base", "RecordModel", "UserModel"]


class RecordModel(Base):
    """SQLAlchemy model for Record entity."""

    __tablename__ = "records"

    # Use String for SQLite testing, PostgresUUID for production
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
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


class UserModel(Base):
    """SQLAlchemy model for User entity."""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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
        """String representation of UserModel."""
        return f"<UserModel(id={self.id}, username={self.username}, email={self.email})>"
