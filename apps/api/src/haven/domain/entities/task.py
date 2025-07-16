"""Task entity - core domain model for TTR system."""

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Task:
    """
    Task entity representing a work item in the TTR system.

    This is the core domain entity that represents a task, todo, or review
    item with tracking information for time-to-resolution.
    """

    id: int | None = None
    title: str = ""
    description: str | None = None
    status: str = "open"
    priority: str = "medium"
    task_type: str = "task"

    # Relationships
    assignee_id: int | None = None
    repository_id: int | None = None

    # Time tracking
    estimated_hours: float | None = None
    actual_hours: float | None = None

    # Dates
    due_date: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Audit fields
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if self.status not in ["open", "in_progress", "completed", "cancelled", "blocked"]:
            raise ValueError(f"Invalid task status: {self.status}")

        if self.priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError(f"Invalid task priority: {self.priority}")

        if self.task_type not in ["task", "todo", "review", "bug", "feature"]:
            raise ValueError(f"Invalid task type: {self.task_type}")

        if self.estimated_hours is not None and self.estimated_hours < 0:
            raise ValueError("Estimated hours cannot be negative")

        if self.actual_hours is not None and self.actual_hours < 0:
            raise ValueError("Actual hours cannot be negative")

        # Ensure timestamps are timezone-aware
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=UTC)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=UTC)

    def start_task(self) -> None:
        """Mark task as started."""
        if self.status == "completed":
            raise ValueError("Cannot start a completed task")

        self.status = "in_progress"
        self.started_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def complete_task(self) -> None:
        """Mark task as completed."""
        if self.status == "completed":
            raise ValueError("Task is already completed")

        self.status = "completed"
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def update_progress(self, hours_worked: float) -> None:
        """Update actual hours worked on the task."""
        if hours_worked < 0:
            raise ValueError("Hours worked cannot be negative")

        self.actual_hours = (self.actual_hours or 0) + hours_worked
        self.updated_at = datetime.now(UTC)

    def get_time_to_resolution(self) -> float | None:
        """Calculate time to resolution in hours."""
        if not self.started_at or not self.completed_at:
            return None

        delta = self.completed_at - self.started_at
        return delta.total_seconds() / 3600  # Convert to hours

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date:
            return False

        return datetime.now(UTC) > self.due_date and self.status != "completed"

    def get_progress_percentage(self) -> float:
        """Calculate progress percentage based on estimated vs actual hours."""
        if not self.estimated_hours or not self.actual_hours:
            return 0.0

        if self.status == "completed":
            return 100.0

        return min(100.0, (self.actual_hours / self.estimated_hours) * 100)

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "task_type": self.task_type,
            "assignee_id": self.assignee_id,
            "repository_id": self.repository_id,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "time_to_resolution": self.get_time_to_resolution(),
            "is_overdue": self.is_overdue(),
            "progress_percentage": self.get_progress_percentage(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Task):
            return NotImplemented
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        if self.id is None:
            return hash(self.title)
        return hash(self.id)
