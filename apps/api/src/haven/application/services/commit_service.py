"""Application service for Commit operations."""

from haven.domain.entities.commit import Commit, CommitReview
from haven.domain.repositories.commit_repository import CommitRepository, CommitReviewRepository


class CommitService:
    """Service for commit operations."""

    def __init__(
        self,
        commit_repository: CommitRepository,
        commit_review_repository: CommitReviewRepository,
    ):
        self.commit_repository = commit_repository
        self.commit_review_repository = commit_review_repository

    async def create_commit(self, commit: Commit) -> Commit:
        """Create a new commit."""
        # Check if commit already exists
        existing = await self.commit_repository.get_by_hash(
            commit.repository_id, commit.commit_hash
        )
        if existing:
            raise ValueError(
                f"Commit {commit.commit_hash} already exists in repository {commit.repository_id}"
            )

        return await self.commit_repository.create(commit)

    async def get_commit_by_id(self, commit_id: int) -> Commit | None:
        """Get a commit by ID."""
        return await self.commit_repository.get_by_id(commit_id)

    async def get_commit_by_hash(self, repository_id: int, commit_hash: str) -> Commit | None:
        """Get a commit by repository and hash."""
        return await self.commit_repository.get_by_hash(repository_id, commit_hash)

    async def get_commits_by_repository(
        self, repository_id: int, limit: int = 100, offset: int = 0
    ) -> list[Commit]:
        """Get commits for a repository."""
        return await self.commit_repository.get_by_repository(repository_id, limit, offset)

    async def update_commit(self, commit: Commit) -> Commit:
        """Update an existing commit."""
        if not commit.id:
            raise ValueError("Commit ID is required for update")

        # Verify commit exists
        existing = await self.commit_repository.get_by_id(commit.id)
        if not existing:
            raise ValueError(f"Commit {commit.id} not found")

        return await self.commit_repository.update(commit)

    async def delete_commit(self, commit_id: int) -> bool:
        """Delete a commit."""
        return await self.commit_repository.delete(commit_id)

    async def sync_commits_from_git(
        self, repository_id: int, git_commits: list[dict]
    ) -> list[Commit]:
        """Sync commits from Git repository data."""
        synced_commits = []

        for git_commit in git_commits:
            # Check if commit already exists
            existing = await self.commit_repository.get_by_hash(repository_id, git_commit["hash"])

            if not existing:
                # Create new commit from Git data
                commit = Commit(
                    repository_id=repository_id,
                    commit_hash=git_commit["hash"],
                    message=git_commit["message"],
                    author_name=git_commit["author_name"],
                    author_email=git_commit["author_email"],
                    committer_name=git_commit["committer_name"],
                    committer_email=git_commit["committer_email"],
                    committed_at=git_commit["committed_at"],
                    diff_stats=git_commit["diff_stats"],
                )

                created_commit = await self.commit_repository.create(commit)
                synced_commits.append(created_commit)
            else:
                synced_commits.append(existing)

        return synced_commits

    # Commit Review methods
    async def create_commit_review(self, review: CommitReview) -> CommitReview:
        """Create a new commit review."""
        # Verify commit exists
        commit = await self.commit_repository.get_by_id(review.commit_id)
        if not commit:
            raise ValueError(f"Commit {review.commit_id} not found")

        return await self.commit_review_repository.create(review)

    async def get_commit_review_by_id(self, review_id: int) -> CommitReview | None:
        """Get a commit review by ID."""
        return await self.commit_review_repository.get_by_id(review_id)

    async def get_reviews_by_commit(self, commit_id: int) -> list[CommitReview]:
        """Get all reviews for a commit."""
        return await self.commit_review_repository.get_by_commit(commit_id)

    async def get_reviews_by_reviewer(
        self, reviewer_id: int, limit: int = 100, offset: int = 0
    ) -> list[CommitReview]:
        """Get reviews by reviewer."""
        return await self.commit_review_repository.get_by_reviewer(reviewer_id, limit, offset)

    async def update_commit_review(self, review: CommitReview) -> CommitReview:
        """Update an existing commit review."""
        if not review.id:
            raise ValueError("Review ID is required for update")

        # Verify review exists
        existing = await self.commit_review_repository.get_by_id(review.id)
        if not existing:
            raise ValueError(f"Review {review.id} not found")

        return await self.commit_review_repository.update(review)

    async def delete_commit_review(self, review_id: int) -> bool:
        """Delete a commit review."""
        return await self.commit_review_repository.delete(review_id)

    async def get_commit_with_reviews(self, commit_id: int) -> dict | None:
        """Get a commit with all its reviews."""
        commit = await self.commit_repository.get_by_id(commit_id)
        if not commit:
            return None

        reviews = await self.commit_review_repository.get_by_commit(commit_id)

        return {
            "commit": commit,
            "reviews": reviews,
            "review_status": self._get_overall_review_status(reviews),
        }

    def _get_overall_review_status(self, reviews: list[CommitReview]) -> str:
        """Determine overall review status from individual reviews."""
        if not reviews:
            return "no_reviews"

        # If any review needs revision, overall status is needs_revision
        if any(review.status.value == "needs_revision" for review in reviews):
            return "needs_revision"

        # If all reviews are approved, overall status is approved
        if all(review.status.value == "approved" for review in reviews):
            return "approved"

        # If any review is pending, overall status is pending
        if any(review.status.value == "pending_review" for review in reviews):
            return "pending_review"

        return "draft"
