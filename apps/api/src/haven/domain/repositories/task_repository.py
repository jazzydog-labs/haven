"""Task repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from haven.domain.entities.task import Task


class TaskRepository(ABC):
    """Abstract repository for Task entities."""

    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Create a new task."""
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get all tasks with pagination."""
        pass

    @abstractmethod
    async def get_by_status(self, status: str, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get tasks by status."""
        pass

    @abstractmethod
    async def get_by_assignee(self, assignee_id: int, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get tasks by assignee."""
        pass

    @abstractmethod
    async def get_by_repository(self, repository_id: int, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get tasks by repository."""
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Update an existing task."""
        pass

    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 100, offset: int = 0) -> List[Task]:
        """Search tasks by title or description."""
        pass

    @abstractmethod
    async def get_overdue_tasks(self, limit: int = 100, offset: int = 0) -> List[Task]:
        """Get overdue tasks."""
        pass

    @abstractmethod
    async def get_task_metrics(self, repository_id: Optional[int] = None) -> dict:
        """Get task metrics and statistics."""
        pass