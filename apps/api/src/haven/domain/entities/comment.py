"""Comment entity - core domain model for TTR system."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Comment:
    """
    Comment entity representing a comment on a task.

    This is the core domain entity that represents comments
    on tasks, todos, or reviews in the TTR system.
    """

    id: int | None = None
    content: str = ""
    comment_type: str = "comment"

    # Relationships
    task_id: int | None = None
    author_id: int | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    # Audit fields
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate comment after initialization."""
        if not self.content or not self.content.strip():
            raise ValueError("Comment content cannot be empty")

        if self.comment_type not in ["comment", "review", "status_change", "time_log"]:
            raise ValueError(f"Invalid comment type: {self.comment_type}")

        if self.task_id is not None and self.task_id <= 0:
            raise ValueError("Task ID must be positive")

        if self.author_id is not None and self.author_id <= 0:
            raise ValueError("Author ID must be positive")

        # Ensure timestamps are timezone-aware
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=UTC)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=UTC)

    def update_content(self, new_content: str) -> None:
        """Update comment content."""
        if not new_content or not new_content.strip():
            raise ValueError("Comment content cannot be empty")

        self.content = new_content
        self.updated_at = datetime.now(UTC)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the comment."""
        self.metadata[key] = value
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        """Convert comment to dictionary representation."""
        return {
            "id": self.id,
            "content": self.content,
            "comment_type": self.comment_type,
            "task_id": self.task_id,
            "author_id": self.author_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Comment):
            return NotImplemented
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        if self.id is None:
            return hash((self.content, self.task_id, self.author_id))
        return hash(self.id)
