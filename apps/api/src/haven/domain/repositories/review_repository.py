"""Repository interfaces for review entities."""

from abc import ABC, abstractmethod

from haven.domain.entities.review_comment import CommitReview, ReviewComment


class ReviewCommentRepository(ABC):
    """Repository interface for ReviewComment entities."""

    @abstractmethod
    async def create(self, review_comment: ReviewComment) -> ReviewComment:
        """Create a new review comment."""
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> ReviewComment | None:
        """Get a review comment by ID."""
        pass

    @abstractmethod
    async def get_by_commit_id(self, commit_id: int) -> list[ReviewComment]:
        """Get all review comments for a commit."""
        pass

    @abstractmethod
    async def get_by_reviewer_id(self, reviewer_id: int) -> list[ReviewComment]:
        """Get all review comments by a specific reviewer."""
        pass

    @abstractmethod
    async def get_by_commit_and_reviewer(
        self, commit_id: int, reviewer_id: int
    ) -> list[ReviewComment]:
        """Get review comments for a commit by a specific reviewer."""
        pass

    @abstractmethod
    async def get_by_file_path(self, commit_id: int, file_path: str) -> list[ReviewComment]:
        """Get review comments for a specific file in a commit."""
        pass

    @abstractmethod
    async def update(self, review_comment: ReviewComment) -> ReviewComment:
        """Update an existing review comment."""
        pass

    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        """Delete a review comment."""
        pass

    @abstractmethod
    async def get_line_comments(
        self, commit_id: int, file_path: str, line_number: int
    ) -> list[ReviewComment]:
        """Get review comments for a specific line in a file."""
        pass


class CommitReviewRepository(ABC):
    """Repository interface for CommitReview entities."""

    @abstractmethod
    async def create(self, commit_review: CommitReview) -> CommitReview:
        """Create a new commit review."""
        pass

    @abstractmethod
    async def get_by_id(self, review_id: int) -> CommitReview | None:
        """Get a commit review by ID."""
        pass

    @abstractmethod
    async def get_by_commit_id(self, commit_id: int) -> list[CommitReview]:
        """Get all reviews for a commit."""
        pass

    @abstractmethod
    async def get_by_reviewer_id(self, reviewer_id: int) -> list[CommitReview]:
        """Get all reviews by a specific reviewer."""
        pass

    @abstractmethod
    async def get_by_commit_and_reviewer(
        self, commit_id: int, reviewer_id: int
    ) -> CommitReview | None:
        """Get a review for a commit by a specific reviewer."""
        pass

    @abstractmethod
    async def get_by_status(self, status: str) -> list[CommitReview]:
        """Get all reviews with a specific status."""
        pass

    @abstractmethod
    async def get_pending_reviews(self, reviewer_id: int | None = None) -> list[CommitReview]:
        """Get all pending reviews, optionally filtered by reviewer."""
        pass

    @abstractmethod
    async def get_completed_reviews(
        self, reviewer_id: int | None = None, limit: int | None = None
    ) -> list[CommitReview]:
        """Get completed reviews, optionally filtered by reviewer with limit."""
        pass

    @abstractmethod
    async def update(self, commit_review: CommitReview) -> CommitReview:
        """Update an existing commit review."""
        pass

    @abstractmethod
    async def delete(self, review_id: int) -> bool:
        """Delete a commit review."""
        pass

    @abstractmethod
    async def get_review_stats(self, reviewer_id: int | None = None) -> dict:
        """Get review statistics (count by status, average time, etc.)."""
        pass

    @abstractmethod
    async def get_commits_needing_review(
        self, repository_id: int | None = None, limit: int | None = None
    ) -> list[int]:
        """Get commit IDs that need review (no pending/completed reviews)."""
        pass
