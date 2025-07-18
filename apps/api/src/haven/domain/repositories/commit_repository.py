"""Repository interface for Commit entities."""

from abc import ABC, abstractmethod

from haven.domain.entities.commit import Commit, CommitReview


class CommitRepository(ABC):
    """Repository interface for Commit entities."""

    @abstractmethod
    async def create(self, commit: Commit) -> Commit:
        """Create a new commit."""
        pass

    @abstractmethod
    async def get_by_id(self, commit_id: int) -> Commit | None:
        """Get a commit by ID."""
        pass

    @abstractmethod
    async def get_by_hash(self, repository_id: int, commit_hash: str) -> Commit | None:
        """Get a commit by repository and hash."""
        pass

    @abstractmethod
    async def get_by_repository(
        self, repository_id: int, limit: int = 100, offset: int = 0
    ) -> list[Commit]:
        """Get commits for a repository."""
        pass

    @abstractmethod
    async def update(self, commit: Commit) -> Commit:
        """Update an existing commit."""
        pass

    @abstractmethod
    async def delete(self, commit_id: int) -> bool:
        """Delete a commit."""
        pass

    @abstractmethod
    async def exists_by_hash(self, repository_id: int, commit_hash: str) -> bool:
        """Check if a commit exists by hash."""
        pass

    @abstractmethod
    async def count_by_repository(self, repository_id: int) -> int:
        """Count commits for a repository."""
        pass


class CommitReviewRepository(ABC):
    """Repository interface for CommitReview entities."""

    @abstractmethod
    async def create(self, review: CommitReview) -> CommitReview:
        """Create a new commit review."""
        pass

    @abstractmethod
    async def get_by_id(self, review_id: int) -> CommitReview | None:
        """Get a commit review by ID."""
        pass

    @abstractmethod
    async def get_by_commit(self, commit_id: int) -> list[CommitReview]:
        """Get all reviews for a commit."""
        pass

    @abstractmethod
    async def get_by_reviewer(
        self, reviewer_id: int, limit: int = 100, offset: int = 0
    ) -> list[CommitReview]:
        """Get reviews by reviewer."""
        pass

    @abstractmethod
    async def update(self, review: CommitReview) -> CommitReview:
        """Update an existing commit review."""
        pass

    @abstractmethod
    async def delete(self, review_id: int) -> bool:
        """Delete a commit review."""
        pass
