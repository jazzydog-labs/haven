"""Milestone entity - core domain model for TTR system."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional


@dataclass
class Milestone:
    """
    Milestone entity representing a roadmap milestone in the TTR system.

    This is the core domain entity that represents a major milestone
    within a roadmap, tracking progress toward specific goals.
    """

    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    status: str = "not_started"
    progress_percentage: int = 0
    
    # Relationships
    roadmap_id: Optional[int] = None
    
    # Dates
    target_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Metrics
    estimated_effort_hours: Optional[float] = None
    actual_effort_hours: Optional[float] = None
    
    # Audit fields
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate milestone after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Milestone title cannot be empty")
        
        if self.status not in ["not_started", "in_progress", "completed", "blocked", "cancelled"]:
            raise ValueError(f"Invalid milestone status: {self.status}")
        
        if self.progress_percentage < 0 or self.progress_percentage > 100:
            raise ValueError("Progress percentage must be between 0 and 100")
        
        if self.estimated_effort_hours is not None and self.estimated_effort_hours < 0:
            raise ValueError("Estimated effort hours cannot be negative")
        
        if self.actual_effort_hours is not None and self.actual_effort_hours < 0:
            raise ValueError("Actual effort hours cannot be negative")
        
        # Ensure timestamps are timezone-aware
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=UTC)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=UTC)
        if self.target_date and self.target_date.tzinfo is None:
            self.target_date = self.target_date.replace(tzinfo=UTC)
        if self.completed_at and self.completed_at.tzinfo is None:
            self.completed_at = self.completed_at.replace(tzinfo=UTC)

    def start(self) -> None:
        """Start working on the milestone."""
        if self.status == "completed":
            raise ValueError("Cannot start a completed milestone")
        if self.status == "cancelled":
            raise ValueError("Cannot start a cancelled milestone")
        
        self.status = "in_progress"
        self.updated_at = datetime.now(UTC)

    def complete(self) -> None:
        """Mark milestone as completed."""
        if self.status == "completed":
            raise ValueError("Milestone is already completed")
        
        self.status = "completed"
        self.progress_percentage = 100
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def block(self) -> None:
        """Mark milestone as blocked."""
        if self.status == "completed":
            raise ValueError("Cannot block a completed milestone")
        if self.status == "cancelled":
            raise ValueError("Cannot block a cancelled milestone")
        
        self.status = "blocked"
        self.updated_at = datetime.now(UTC)

    def cancel(self) -> None:
        """Cancel the milestone."""
        if self.status == "completed":
            raise ValueError("Cannot cancel a completed milestone")
        
        self.status = "cancelled"
        self.updated_at = datetime.now(UTC)

    def update_progress(self, progress_percentage: int) -> None:
        """Update milestone progress."""
        if progress_percentage < 0 or progress_percentage > 100:
            raise ValueError("Progress percentage must be between 0 and 100")
        
        self.progress_percentage = progress_percentage
        
        # Auto-update status based on progress
        if progress_percentage == 0 and self.status == "in_progress":
            self.status = "not_started"
        elif progress_percentage > 0 and progress_percentage < 100 and self.status == "not_started":
            self.status = "in_progress"
        elif progress_percentage == 100 and self.status != "completed":
            self.complete()
        else:
            self.updated_at = datetime.now(UTC)

    def update_effort(self, actual_hours: float) -> None:
        """Update actual effort hours."""
        if actual_hours < 0:
            raise ValueError("Actual effort hours cannot be negative")
        
        self.actual_effort_hours = actual_hours
        self.updated_at = datetime.now(UTC)

    def is_overdue(self) -> bool:
        """Check if milestone is overdue."""
        if not self.target_date:
            return False
        
        return datetime.now(UTC) > self.target_date and self.status != "completed"

    def get_effort_variance(self) -> Optional[float]:
        """Get variance between estimated and actual effort."""
        if self.estimated_effort_hours is None or self.actual_effort_hours is None:
            return None
        
        return self.actual_effort_hours - self.estimated_effort_hours

    def get_effort_variance_percentage(self) -> Optional[float]:
        """Get effort variance as a percentage."""
        if self.estimated_effort_hours is None or self.estimated_effort_hours == 0:
            return None
        
        variance = self.get_effort_variance()
        if variance is None:
            return None
        
        return (variance / self.estimated_effort_hours) * 100

    def to_dict(self) -> dict:
        """Convert milestone to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "roadmap_id": self.roadmap_id,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "estimated_effort_hours": self.estimated_effort_hours,
            "actual_effort_hours": self.actual_effort_hours,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_overdue": self.is_overdue(),
            "effort_variance": self.get_effort_variance(),
            "effort_variance_percentage": self.get_effort_variance_percentage(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Milestone):
            return NotImplemented
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        if self.id is None:
            return hash(self.title)
        return hash(self.id)