"""TimeLog entity - core domain model for TTR system."""

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class TimeLog:
    """
    TimeLog entity representing time spent on a task.

    This is the core domain entity that represents time logging
    for tasks, todos, or reviews in the TTR system.
    """

    id: int | None = None
    description: str | None = None
    hours: float = 0.0
    log_type: str = "work"

    # Relationships
    task_id: int | None = None
    user_id: int | None = None

    # Date tracking
    logged_date: datetime = field(default_factory=lambda: datetime.now(UTC))

    # Audit fields
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate time log after initialization."""
        if self.hours < 0:
            raise ValueError("Hours cannot be negative")

        if self.hours > 24:
            raise ValueError("Hours cannot exceed 24 in a single log entry")

        if self.log_type not in ["work", "review", "testing", "documentation", "meeting"]:
            raise ValueError(f"Invalid log type: {self.log_type}")

        if self.task_id is not None and self.task_id <= 0:
            raise ValueError("Task ID must be positive")

        if self.user_id is not None and self.user_id <= 0:
            raise ValueError("User ID must be positive")

        # Ensure timestamps are timezone-aware
        if self.logged_date and self.logged_date.tzinfo is None:
            self.logged_date = self.logged_date.replace(tzinfo=UTC)
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=UTC)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=UTC)

    def update_hours(self, new_hours: float) -> None:
        """Update the hours logged."""
        if new_hours < 0:
            raise ValueError("Hours cannot be negative")

        if new_hours > 24:
            raise ValueError("Hours cannot exceed 24 in a single log entry")

        self.hours = new_hours
        self.updated_at = datetime.now(UTC)

    def update_description(self, new_description: str) -> None:
        """Update the description of the time log."""
        self.description = new_description
        self.updated_at = datetime.now(UTC)

    def is_today(self) -> bool:
        """Check if the time log is for today."""
        today = datetime.now(UTC).date()
        return self.logged_date.date() == today

    def is_this_week(self) -> bool:
        """Check if the time log is from this week."""
        today = datetime.now(UTC).date()
        days_since_monday = today.weekday()
        week_start = today - datetime.timedelta(days=days_since_monday)
        return self.logged_date.date() >= week_start

    def get_efficiency_score(self) -> float:
        """Calculate efficiency score based on log type and hours."""
        type_multipliers = {
            "work": 1.0,
            "review": 0.8,
            "testing": 0.9,
            "documentation": 0.7,
            "meeting": 0.5,
        }

        multiplier = type_multipliers.get(self.log_type, 1.0)
        return self.hours * multiplier

    def to_dict(self) -> dict:
        """Convert time log to dictionary representation."""
        return {
            "id": self.id,
            "description": self.description,
            "hours": self.hours,
            "log_type": self.log_type,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "logged_date": self.logged_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_today": self.is_today(),
            "is_this_week": self.is_this_week(),
            "efficiency_score": self.get_efficiency_score(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, TimeLog):
            return NotImplemented
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        if self.id is None:
            return hash((self.task_id, self.user_id, self.logged_date, self.hours))
        return hash(self.id)
