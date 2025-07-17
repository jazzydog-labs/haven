"""Comment repository interface."""

from abc import ABC, abstractmethod

from haven.domain.entities.comment import Comment


class CommentRepository(ABC):
    """Abstract repository for Comment entities."""

    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        """Create a new comment."""
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Comment | None:
        """Get a comment by its ID."""
        pass

    @abstractmethod
    async def get_by_task(self, task_id: int, limit: int = 100, offset: int = 0) -> list[Comment]:
        """Get comments for a specific task."""
        pass

    @abstractmethod
    async def get_by_author(
        self, author_id: int, limit: int = 100, offset: int = 0
    ) -> list[Comment]:
        """Get comments by author."""
        pass

    @abstractmethod
    async def get_by_type(
        self, comment_type: str, limit: int = 100, offset: int = 0
    ) -> list[Comment]:
        """Get comments by type."""
        pass

    @abstractmethod
    async def update(self, comment: Comment) -> Comment:
        """Update an existing comment."""
        pass

    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        """Delete a comment by its ID."""
        pass

    @abstractmethod
    async def get_recent_comments(self, limit: int = 10) -> list[Comment]:
        """Get recent comments across all tasks."""
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 100, offset: int = 0) -> list[Comment]:
        """Search comments by content."""
        pass
