"""Commit domain entity for TTR system."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ReviewStatus(Enum):
    """Status of a commit review."""

    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    DRAFT = "draft"


@dataclass
class DiffStats:
    """Statistics about changes in a commit."""

    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0

    @property
    def total_changes(self) -> int:
        """Total number of line changes."""
        return self.insertions + self.deletions


@dataclass
class Commit:
    """
    Represents a Git commit within a tracked repository.

    This entity tracks commit metadata, diff statistics, and review status
    for integration with the TTR system.
    """

    repository_id: int
    commit_hash: str
    message: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    committed_at: datetime
    diff_stats: DiffStats

    # Optional fields
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # Diff HTML file reference
    diff_html_path: str | None = None
    diff_generated_at: datetime | None = None

    def __post_init__(self):
        """Validate commit data after initialization."""
        if not self.commit_hash:
            raise ValueError("Commit hash is required")
        if len(self.commit_hash) < 7:
            raise ValueError("Commit hash must be at least 7 characters")
        if not self.message:
            raise ValueError("Commit message is required")
        if not self.author_name:
            raise ValueError("Author name is required")
        if not self.author_email:
            raise ValueError("Author email is required")
        if not self.committer_name:
            raise ValueError("Committer name is required")
        if not self.committer_email:
            raise ValueError("Committer email is required")
        if self.repository_id <= 0:
            raise ValueError("Repository ID must be positive")

    @property
    def short_hash(self) -> str:
        """Return the short version of the commit hash."""
        return self.commit_hash[:7]

    @property
    def is_merge_commit(self) -> bool:
        """Check if this is a merge commit based on the message."""
        return self.message.startswith("Merge ")

    @property
    def summary(self) -> str:
        """Return the first line of the commit message."""
        return self.message.split("\n")[0]


@dataclass
class CommitReview:
    """
    Represents a review of a Git commit.

    This entity tracks the review status and metadata for commits
    within the TTR system.
    """

    commit_id: int
    reviewer_id: int
    status: ReviewStatus

    # Optional fields
    id: int | None = None
    notes: str | None = None
    reviewed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self):
        """Validate review data after initialization."""
        if self.commit_id <= 0:
            raise ValueError("Commit ID must be positive")
        if self.reviewer_id <= 0:
            raise ValueError("Reviewer ID must be positive")
        if not isinstance(self.status, ReviewStatus):
            raise ValueError("Status must be a valid ReviewStatus")

    @property
    def is_approved(self) -> bool:
        """Check if the review is approved."""
        return self.status == ReviewStatus.APPROVED

    @property
    def needs_action(self) -> bool:
        """Check if the review needs action from the author."""
        return self.status in [ReviewStatus.PENDING_REVIEW, ReviewStatus.NEEDS_REVISION]
