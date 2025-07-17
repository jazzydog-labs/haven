"""Review comment domain entity."""

from datetime import UTC, datetime
from typing import ClassVar

from pydantic import BaseModel, Field, field_validator


class ReviewComment(BaseModel):
    """Domain entity for review comments on commits."""

    id: int | None = None
    commit_id: int = Field(..., description="ID of the commit being reviewed")
    reviewer_id: int = Field(..., description="ID of the user making the comment")
    line_number: int | None = Field(None, description="Line number for line-specific comments")
    file_path: str | None = Field(
        None, max_length=500, description="File path for file-specific comments"
    )
    content: str = Field(..., min_length=1, max_length=10000, description="Comment content")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    class Config:
        """Pydantic configuration."""

        frozen = True
        json_schema_extra: ClassVar[dict] = {
            "example": {
                "commit_id": 1,
                "reviewer_id": 1,
                "line_number": 42,
                "file_path": "src/main.py",
                "content": "Consider adding error handling here for better robustness.",
            }
        }

    @field_validator("line_number")
    @classmethod
    def validate_line_number(cls, v):
        """Validate line number is positive."""
        if v is not None and v <= 0:
            raise ValueError("Line number must be positive")
        return v

    @field_validator("file_path")
    @classmethod
    def validate_file_path(cls, v):
        """Validate file path format."""
        if v is not None:
            if v.startswith("/"):
                raise ValueError("File path should be relative (not start with /)")
            if ".." in v:
                raise ValueError("File path cannot contain .. sequences")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        """Validate comment content."""
        if not v.strip():
            raise ValueError("Comment content cannot be empty or whitespace only")
        return v.strip()

    @property
    def is_line_comment(self) -> bool:
        """Check if this is a line-specific comment."""
        return self.line_number is not None

    @property
    def is_file_comment(self) -> bool:
        """Check if this is a file-specific comment."""
        return self.file_path is not None and self.line_number is None

    @property
    def is_general_comment(self) -> bool:
        """Check if this is a general commit comment."""
        return self.file_path is None and self.line_number is None

    def update_content(self, new_content: str) -> "ReviewComment":
        """Create updated comment with new content."""
        return self.__class__(
            **{**self.dict(), "content": new_content, "updated_at": datetime.now(UTC)}
        )


class CommitReview(BaseModel):
    """Domain entity for commit review status tracking."""

    class ReviewStatus:
        """Valid review status values."""

        DRAFT = "draft"
        PENDING = "pending"
        APPROVED = "approved"
        NEEDS_REVISION = "needs_revision"

        @classmethod
        def all_values(cls) -> list[str]:
            """Get all valid status values."""
            return [cls.DRAFT, cls.PENDING, cls.APPROVED, cls.NEEDS_REVISION]

    id: int | None = None
    commit_id: int = Field(..., description="ID of the commit being reviewed")
    reviewer_id: int = Field(..., description="ID of the reviewer")
    status: str = Field(..., description="Review status")
    reviewed_at: datetime | None = Field(None, description="When the review was completed")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        """Pydantic configuration."""

        frozen = True
        json_schema_extra: ClassVar[dict] = {
            "example": {
                "commit_id": 1,
                "reviewer_id": 1,
                "status": "approved",
                "reviewed_at": "2025-07-17T10:30:00Z",
            }
        }

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Validate review status."""
        if v not in cls.ReviewStatus.all_values():
            raise ValueError(f"Status must be one of {cls.ReviewStatus.all_values()}")
        return v

    @property
    def is_completed(self) -> bool:
        """Check if review is completed (approved or needs revision)."""
        return self.status in [self.ReviewStatus.APPROVED, self.ReviewStatus.NEEDS_REVISION]

    @property
    def is_pending(self) -> bool:
        """Check if review is pending."""
        return self.status == self.ReviewStatus.PENDING

    @property
    def is_draft(self) -> bool:
        """Check if review is in draft state."""
        return self.status == self.ReviewStatus.DRAFT

    def complete_review(self, status: str) -> "CommitReview":
        """Complete the review with a final status."""
        if status not in [self.ReviewStatus.APPROVED, self.ReviewStatus.NEEDS_REVISION]:
            raise ValueError("Complete review status must be approved or needs_revision")

        return self.__class__(**{**self.dict(), "status": status, "reviewed_at": datetime.now(UTC)})

    def update_status(self, new_status: str) -> "CommitReview":
        """Update review status."""
        return self.__class__(
            **{
                **self.dict(),
                "status": new_status,
                "reviewed_at": datetime.now(UTC)
                if new_status in [self.ReviewStatus.APPROVED, self.ReviewStatus.NEEDS_REVISION]
                else self.reviewed_at,
            }
        )
