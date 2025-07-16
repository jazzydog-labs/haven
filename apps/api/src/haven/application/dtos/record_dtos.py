"""DTOs for Record operations."""

from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

from pydantic import BaseModel, Field


class RecordCreateDTO(BaseModel):
    """DTO for creating a record."""

    data: dict[str, Any] = Field(default_factory=dict, description="Record data")

    class Config:
        """Pydantic configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "data": {
                    "name": "Example Record",
                    "description": "This is an example",
                    "metadata": {"tags": ["example", "test"]},
                }
            }
        }


class RecordUpdateDTO(BaseModel):
    """DTO for updating a record."""

    data: dict[str, Any] = Field(..., description="New record data")

    class Config:
        """Pydantic configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "data": {
                    "name": "Updated Record",
                    "description": "This has been updated",
                    "metadata": {"tags": ["updated"]},
                }
            }
        }


class RecordResponseDTO(BaseModel):
    """DTO for record responses."""

    id: UUID = Field(..., description="Record UUID")
    data: dict[str, Any] = Field(..., description="Record data")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "name": "Example Record",
                    "description": "This is an example",
                },
                "created_at": "2025-01-15T12:00:00Z",
                "updated_at": "2025-01-15T12:00:00Z",
            }
        }


class RecordListResponseDTO(BaseModel):
    """DTO for paginated record list responses."""

    items: list[RecordResponseDTO] = Field(..., description="List of records")
    total: int = Field(..., description="Total number of records")
    limit: int = Field(..., description="Maximum records per page")
    offset: int = Field(..., description="Number of records skipped")

    class Config:
        """Pydantic configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "items": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "data": {"name": "Record 1"},
                        "created_at": "2025-01-15T12:00:00Z",
                        "updated_at": "2025-01-15T12:00:00Z",
                    }
                ],
                "total": 100,
                "limit": 20,
                "offset": 0,
            }
        }
