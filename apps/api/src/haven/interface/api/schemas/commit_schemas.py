"""Pydantic schemas for commit API endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field

from haven.domain.entities.commit import Commit, CommitReview, DiffStats, ReviewStatus


class DiffStatsSchema(BaseModel):
    """Schema for diff statistics."""

    files_changed: int = Field(default=0, ge=0)
    insertions: int = Field(default=0, ge=0)
    deletions: int = Field(default=0, ge=0)

    @classmethod
    def from_entity(cls, stats: DiffStats) -> "DiffStatsSchema":
        """Create from domain entity."""
        return cls(
            files_changed=stats.files_changed,
            insertions=stats.insertions,
            deletions=stats.deletions,
        )


class CommitBase(BaseModel):
    """Base schema for commit data."""

    repository_id: int = Field(..., gt=0)
    commit_hash: str = Field(..., min_length=7, max_length=64)
    message: str = Field(..., min_length=1)
    author_name: str = Field(..., min_length=1)
    author_email: str = Field(..., min_length=1)
    committer_name: str = Field(..., min_length=1)
    committer_email: str = Field(..., min_length=1)
    committed_at: datetime


class CommitCreate(CommitBase):
    """Schema for creating a commit."""

    diff_stats: DiffStats = Field(default_factory=DiffStats)


class CommitResponse(CommitBase):
    """Schema for commit response."""

    id: int
    diff_stats: DiffStatsSchema
    diff_html_path: str | None = None
    diff_generated_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True

    @classmethod
    def from_entity(cls, commit: Commit) -> "CommitResponse":
        """Create from domain entity."""
        return cls(
            id=commit.id,
            repository_id=commit.repository_id,
            commit_hash=commit.commit_hash,
            message=commit.message,
            author_name=commit.author_name,
            author_email=commit.author_email,
            committer_name=commit.committer_name,
            committer_email=commit.committer_email,
            committed_at=commit.committed_at,
            diff_stats=DiffStatsSchema.from_entity(commit.diff_stats),
            diff_html_path=commit.diff_html_path,
            diff_generated_at=commit.diff_generated_at,
            created_at=commit.created_at,
            updated_at=commit.updated_at,
        )


class CommitDiffResponse(BaseModel):
    """Response for diff generation."""

    commit_id: int
    diff_html_path: str
    diff_generated_at: datetime | None


class CommitReviewBase(BaseModel):
    """Base schema for commit review."""

    reviewer_id: int = Field(..., gt=0)
    status: ReviewStatus
    notes: str | None = None


class CommitReviewCreate(CommitReviewBase):
    """Schema for creating a commit review."""

    pass


class CommitReviewResponse(CommitReviewBase):
    """Schema for commit review response."""

    id: int
    commit_id: int
    reviewed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True

    @classmethod
    def from_entity(cls, review: CommitReview) -> "CommitReviewResponse":
        """Create from domain entity."""
        return cls(
            id=review.id,
            commit_id=review.commit_id,
            reviewer_id=review.reviewer_id,
            status=review.status,
            notes=review.notes,
            reviewed_at=review.reviewed_at,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
