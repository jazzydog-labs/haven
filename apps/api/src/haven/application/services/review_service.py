"""Service layer for review management and workflows."""

from haven.domain.entities.review_comment import CommitReview, ReviewComment
from haven.domain.repositories.commit_repository import CommitRepository
from haven.domain.repositories.review_repository import (
    CommitReviewRepository,
    ReviewCommentRepository,
)
from haven.domain.repositories.user_repository import UserRepository


class ReviewService:
    """Service for managing commit reviews and comments."""

    def __init__(
        self,
        review_comment_repo: ReviewCommentRepository,
        commit_review_repo: CommitReviewRepository,
        commit_repo: CommitRepository,
        user_repo: UserRepository,
    ):
        self.review_comment_repo = review_comment_repo
        self.commit_review_repo = commit_review_repo
        self.commit_repo = commit_repo
        self.user_repo = user_repo

    # Review Comment Operations

    async def create_review_comment(
        self,
        commit_id: int,
        reviewer_id: int,
        content: str,
        file_path: str | None = None,
        line_number: int | None = None,
    ) -> ReviewComment:
        """Create a new review comment."""
        # Validate commit exists
        commit = await self.commit_repo.get_by_id(commit_id)
        if not commit:
            raise ValueError(f"Commit with ID {commit_id} not found")

        # Validate reviewer exists
        reviewer = await self.user_repo.get_by_id(reviewer_id)
        if not reviewer:
            raise ValueError(f"User with ID {reviewer_id} not found")

        comment = ReviewComment(
            commit_id=commit_id,
            reviewer_id=reviewer_id,
            content=content,
            file_path=file_path,
            line_number=line_number,
        )

        return await self.review_comment_repo.create(comment)

    async def get_review_comment(self, comment_id: int) -> ReviewComment | None:
        """Get a review comment by ID."""
        return await self.review_comment_repo.get_by_id(comment_id)

    async def get_commit_comments(self, commit_id: int) -> list[ReviewComment]:
        """Get all review comments for a commit."""
        return await self.review_comment_repo.get_by_commit_id(commit_id)

    async def get_file_comments(self, commit_id: int, file_path: str) -> list[ReviewComment]:
        """Get all review comments for a specific file in a commit."""
        return await self.review_comment_repo.get_by_file_path(commit_id, file_path)

    async def get_line_comments(
        self, commit_id: int, file_path: str, line_number: int
    ) -> list[ReviewComment]:
        """Get all review comments for a specific line in a file."""
        return await self.review_comment_repo.get_line_comments(commit_id, file_path, line_number)

    async def update_review_comment(
        self, comment_id: int, new_content: str, reviewer_id: int
    ) -> ReviewComment:
        """Update a review comment's content."""
        existing = await self.review_comment_repo.get_by_id(comment_id)
        if not existing:
            raise ValueError(f"Review comment with ID {comment_id} not found")

        # Only allow the original reviewer to update
        if existing.reviewer_id != reviewer_id:
            raise ValueError("Only the original reviewer can update this comment")

        updated_comment = existing.update_content(new_content)
        return await self.review_comment_repo.update(updated_comment)

    async def delete_review_comment(self, comment_id: int, reviewer_id: int) -> bool:
        """Delete a review comment."""
        existing = await self.review_comment_repo.get_by_id(comment_id)
        if not existing:
            raise ValueError(f"Review comment with ID {comment_id} not found")

        # Only allow the original reviewer to delete
        if existing.reviewer_id != reviewer_id:
            raise ValueError("Only the original reviewer can delete this comment")

        return await self.review_comment_repo.delete(comment_id)

    # Commit Review Operations

    async def create_commit_review(
        self, commit_id: int, reviewer_id: int, status: str = CommitReview.ReviewStatus.DRAFT
    ) -> CommitReview:
        """Create a new commit review."""
        # Validate commit exists
        commit = await self.commit_repo.get_by_id(commit_id)
        if not commit:
            raise ValueError(f"Commit with ID {commit_id} not found")

        # Validate reviewer exists
        reviewer = await self.user_repo.get_by_id(reviewer_id)
        if not reviewer:
            raise ValueError(f"User with ID {reviewer_id} not found")

        # Check if review already exists for this commit/reviewer
        existing = await self.commit_review_repo.get_by_commit_and_reviewer(commit_id, reviewer_id)
        if existing:
            raise ValueError(
                f"Review already exists for commit {commit_id} by reviewer {reviewer_id}"
            )

        review = CommitReview(commit_id=commit_id, reviewer_id=reviewer_id, status=status)

        return await self.commit_review_repo.create(review)

    async def get_commit_review(self, review_id: int) -> CommitReview | None:
        """Get a commit review by ID."""
        return await self.commit_review_repo.get_by_id(review_id)

    async def get_commit_reviews(self, commit_id: int) -> list[CommitReview]:
        """Get all reviews for a commit."""
        return await self.commit_review_repo.get_by_commit_id(commit_id)

    async def get_reviewer_reviews(self, reviewer_id: int) -> list[CommitReview]:
        """Get all reviews by a specific reviewer."""
        return await self.commit_review_repo.get_by_reviewer_id(reviewer_id)

    async def get_pending_reviews(self, reviewer_id: int | None = None) -> list[CommitReview]:
        """Get pending reviews, optionally filtered by reviewer."""
        return await self.commit_review_repo.get_pending_reviews(reviewer_id)

    async def approve_commit(self, commit_id: int, reviewer_id: int) -> CommitReview:
        """Approve a commit review."""
        return await self._update_review_status(
            commit_id, reviewer_id, CommitReview.ReviewStatus.APPROVED
        )

    async def request_changes(self, commit_id: int, reviewer_id: int) -> CommitReview:
        """Request changes for a commit review."""
        return await self._update_review_status(
            commit_id, reviewer_id, CommitReview.ReviewStatus.NEEDS_REVISION
        )

    async def submit_for_review(self, commit_id: int, reviewer_id: int) -> CommitReview:
        """Submit a draft review for review."""
        return await self._update_review_status(
            commit_id, reviewer_id, CommitReview.ReviewStatus.PENDING
        )

    async def _update_review_status(
        self, commit_id: int, reviewer_id: int, new_status: str
    ) -> CommitReview:
        """Update the status of a commit review."""
        existing = await self.commit_review_repo.get_by_commit_and_reviewer(commit_id, reviewer_id)
        if not existing:
            raise ValueError(f"No review found for commit {commit_id} by reviewer {reviewer_id}")

        if new_status in [
            CommitReview.ReviewStatus.APPROVED,
            CommitReview.ReviewStatus.NEEDS_REVISION,
        ]:
            updated_review = existing.complete_review(new_status)
        else:
            updated_review = existing.update_status(new_status)

        return await self.commit_review_repo.update(updated_review)

    # Review Analytics and Workflows

    async def get_review_statistics(self, reviewer_id: int | None = None) -> dict:
        """Get review statistics."""
        stats = await self.commit_review_repo.get_review_stats(reviewer_id)

        # Add computed metrics
        total = stats["total_reviews"]
        if total > 0:
            stats["completion_rate"] = (
                stats["status_counts"].get(CommitReview.ReviewStatus.APPROVED, 0)
                + stats["status_counts"].get(CommitReview.ReviewStatus.NEEDS_REVISION, 0)
            ) / total
            stats["approval_rate"] = (
                stats["status_counts"].get(CommitReview.ReviewStatus.APPROVED, 0) / total
            )
        else:
            stats["completion_rate"] = 0.0
            stats["approval_rate"] = 0.0

        return stats

    async def get_commits_needing_review(
        self, repository_id: int | None = None, limit: int = 50
    ) -> list[int]:
        """Get commit IDs that need review."""
        return await self.commit_review_repo.get_commits_needing_review(repository_id, limit)

    async def get_review_workload(self, reviewer_id: int) -> dict:
        """Get review workload summary for a reviewer."""
        pending = await self.commit_review_repo.get_pending_reviews(reviewer_id)
        completed = await self.commit_review_repo.get_completed_reviews(reviewer_id, limit=10)
        stats = await self.get_review_statistics(reviewer_id)

        return {
            "pending_count": len(pending),
            "pending_reviews": pending,
            "recent_completed": completed,
            "statistics": stats,
        }

    async def bulk_approve_commits(
        self, commit_ids: list[int], reviewer_id: int
    ) -> list[CommitReview]:
        """Approve multiple commits in bulk."""
        results = []
        errors = []

        for commit_id in commit_ids:
            try:
                review = await self.approve_commit(commit_id, reviewer_id)
                results.append(review)
            except Exception as e:
                errors.append({"commit_id": commit_id, "error": str(e)})

        if errors:
            # Log errors but return successful results
            # In a real application, you might want to use proper logging
            print(f"Bulk approval errors: {errors}")

        return results
