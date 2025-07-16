"""Todo entity - core domain model for TTR system."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Optional


@dataclass
class Todo:
    """
    Todo entity representing a todo item in the TTR system.

    This is the core domain entity that represents a simple todo item
    that can be standalone or linked to tasks and milestones.
    """

    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    is_completed: bool = False
    priority: str = "medium"
    category: str = "general"
    
    # Relationships
    owner_id: Optional[int] = None
    task_id: Optional[int] = None
    milestone_id: Optional[int] = None
    
    # Dates
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Metadata
    tags: dict[str, Any] = field(default_factory=dict)
    
    # Audit fields
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate todo after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Todo title cannot be empty")
        
        if self.priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError(f"Invalid todo priority: {self.priority}")
        
        # Ensure timestamps are timezone-aware
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=UTC)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=UTC)
        if self.due_date and self.due_date.tzinfo is None:
            self.due_date = self.due_date.replace(tzinfo=UTC)
        if self.completed_at and self.completed_at.tzinfo is None:
            self.completed_at = self.completed_at.replace(tzinfo=UTC)

    def complete(self) -> None:
        """Mark todo as completed."""
        if self.is_completed:
            raise ValueError("Todo is already completed")
        
        self.is_completed = True
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def uncomplete(self) -> None:
        """Mark todo as not completed."""
        if not self.is_completed:
            raise ValueError("Todo is not completed")
        
        self.is_completed = False
        self.completed_at = None
        self.updated_at = datetime.now(UTC)

    def update_priority(self, priority: str) -> None:
        """Update todo priority."""
        if priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError(f"Invalid todo priority: {priority}")
        
        self.priority = priority
        self.updated_at = datetime.now(UTC)

    def add_tag(self, key: str, value: Any) -> None:
        """Add a tag to the todo."""
        self.tags[key] = value
        self.updated_at = datetime.now(UTC)

    def remove_tag(self, key: str) -> None:
        """Remove a tag from the todo."""
        if key in self.tags:
            del self.tags[key]
            self.updated_at = datetime.now(UTC)

    def is_overdue(self) -> bool:
        """Check if todo is overdue."""
        if not self.due_date:
            return False
        
        return datetime.now(UTC) > self.due_date and not self.is_completed

    def to_dict(self) -> dict:
        """Convert todo to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "priority": self.priority,
            "category": self.category,
            "owner_id": self.owner_id,
            "task_id": self.task_id,
            "milestone_id": self.milestone_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_overdue": self.is_overdue(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Todo):
            return NotImplemented
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        if self.id is None:
            return hash(self.title)
        return hash(self.id)