"""Roadmap entity - core domain model for TTR system."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Roadmap:
    """
    Roadmap entity representing a project roadmap in the TTR system.

    This is the core domain entity that represents a high-level roadmap
    containing milestones and tracking overall project progress.
    """

    id: int | None = None
    name: str = ""
    description: str | None = None
    vision: str | None = None
    status: str = "planning"

    # Relationships
    owner_id: int | None = None
    repository_id: int | None = None

    # Dates
    start_date: datetime | None = None
    end_date: datetime | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    # Audit fields
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate roadmap after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Roadmap name cannot be empty")

        if self.status not in ["planning", "active", "paused", "completed", "cancelled"]:
            raise ValueError(f"Invalid roadmap status: {self.status}")

        # Ensure timestamps are timezone-aware
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=UTC)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=UTC)
        if self.start_date and self.start_date.tzinfo is None:
            self.start_date = self.start_date.replace(tzinfo=UTC)
        if self.end_date and self.end_date.tzinfo is None:
            self.end_date = self.end_date.replace(tzinfo=UTC)

    def activate(self) -> None:
        """Activate the roadmap."""
        if self.status == "completed":
            raise ValueError("Cannot activate a completed roadmap")
        if self.status == "cancelled":
            raise ValueError("Cannot activate a cancelled roadmap")

        self.status = "active"
        if not self.start_date:
            self.start_date = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def pause(self) -> None:
        """Pause the roadmap."""
        if self.status != "active":
            raise ValueError("Can only pause an active roadmap")

        self.status = "paused"
        self.updated_at = datetime.now(UTC)

    def complete(self) -> None:
        """Mark roadmap as completed."""
        if self.status == "completed":
            raise ValueError("Roadmap is already completed")

        self.status = "completed"
        if not self.end_date:
            self.end_date = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def cancel(self) -> None:
        """Cancel the roadmap."""
        if self.status == "completed":
            raise ValueError("Cannot cancel a completed roadmap")

        self.status = "cancelled"
        self.updated_at = datetime.now(UTC)

    def update_dates(self, start_date: datetime | None = None, end_date: datetime | None = None) -> None:
        """Update roadmap dates."""
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        if start_date:
            self.start_date = start_date if start_date.tzinfo else start_date.replace(tzinfo=UTC)
        if end_date:
            self.end_date = end_date if end_date.tzinfo else end_date.replace(tzinfo=UTC)

        self.updated_at = datetime.now(UTC)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the roadmap."""
        self.metadata[key] = value
        self.updated_at = datetime.now(UTC)

    def get_duration_days(self) -> int | None:
        """Get roadmap duration in days."""
        if not self.start_date:
            return None

        end = self.end_date or datetime.now(UTC)
        delta = end - self.start_date
        return delta.days

    def is_overdue(self) -> bool:
        """Check if roadmap is overdue."""
        if not self.end_date:
            return False

        return datetime.now(UTC) > self.end_date and self.status not in ["completed", "cancelled"]

    def to_dict(self) -> dict:
        """Convert roadmap to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "vision": self.vision,
            "status": self.status,
            "owner_id": self.owner_id,
            "repository_id": self.repository_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "duration_days": self.get_duration_days(),
            "is_overdue": self.is_overdue(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Roadmap):
            return NotImplemented
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        if self.id is None:
            return hash(self.name)
        return hash(self.id)
