"""Record entity - core domain model."""

import copy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class Record:
    """
    Record entity representing arbitrary JSON data.
    
    This is the core domain entity that represents a record
    with a unique ID and arbitrary JSON data payload.
    """

    id: UUID = field(default_factory=uuid4)
    data: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        """Validate record after initialization."""
        if not isinstance(self.data, dict):
            raise ValueError("Record data must be a dictionary")
        
        # Deep copy the data to ensure isolation
        self.data = copy.deepcopy(self.data)
        
        # Ensure timestamps are timezone-aware
        if self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
        if self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=timezone.utc)

    def update_data(self, new_data: dict[str, Any]) -> None:
        """
        Update the record's data and timestamp.
        
        Args:
            new_data: New data to replace the existing data
            
        Raises:
            ValueError: If new_data is not a dictionary
        """
        if not isinstance(new_data, dict):
            raise ValueError("New data must be a dictionary")
        
        self.data = new_data
        self.updated_at = datetime.now(timezone.utc)

    def merge_data(self, partial_data: dict[str, Any]) -> None:
        """
        Merge partial data into the record's existing data.
        
        Args:
            partial_data: Data to merge with existing data
            
        Raises:
            ValueError: If partial_data is not a dictionary
        """
        if not isinstance(partial_data, dict):
            raise ValueError("Partial data must be a dictionary")
        
        self.data.update(partial_data)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert record to dictionary representation.
        
        Returns:
            Dictionary with id, data, created_at, and updated_at
        """
        return {
            "id": str(self.id),
            "data": self.data,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Record):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        return hash(self.id)