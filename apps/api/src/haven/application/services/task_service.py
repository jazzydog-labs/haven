"""Task service for TTR system."""

from datetime import datetime

from haven.domain.entities.task import Task
from haven.domain.repositories.task_repository import TaskRepository


class TaskService:
    """Service for managing tasks in the TTR system."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(
        self,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        task_type: str = "task",
        assignee_id: int | None = None,
        repository_id: int | None = None,
        estimated_hours: float | None = None,
        due_date: datetime | None = None,
    ) -> Task:
        """Create a new task."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            task_type=task_type,
            assignee_id=assignee_id,
            repository_id=repository_id,
            estimated_hours=estimated_hours,
            due_date=due_date,
        )

        return await self.task_repository.create(task)

    async def get_task_by_id(self, task_id: int) -> Task | None:
        """Get a task by its ID."""
        return await self.task_repository.get_by_id(task_id)

    async def get_all_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get all tasks with pagination."""
        return await self.task_repository.get_all(limit=limit, offset=offset)

    async def get_tasks_by_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        """Get tasks by status."""
        return await self.task_repository.get_by_status(status, limit=limit, offset=offset)

    async def get_tasks_by_assignee(
        self, assignee_id: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        """Get tasks assigned to a specific user."""
        return await self.task_repository.get_by_assignee(assignee_id, limit=limit, offset=offset)

    async def get_tasks_by_repository(
        self, repository_id: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        """Get tasks for a specific repository."""
        return await self.task_repository.get_by_repository(
            repository_id, limit=limit, offset=offset
        )

    async def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        task_type: str | None = None,
        assignee_id: int | None = None,
        repository_id: int | None = None,
        estimated_hours: float | None = None,
        actual_hours: float | None = None,
        due_date: datetime | None = None,
    ) -> Task:
        """Update a task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Update only provided fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if task_type is not None:
            task.task_type = task_type
        if assignee_id is not None:
            task.assignee_id = assignee_id
        if repository_id is not None:
            task.repository_id = repository_id
        if estimated_hours is not None:
            task.estimated_hours = estimated_hours
        if actual_hours is not None:
            task.actual_hours = actual_hours
        if due_date is not None:
            task.due_date = due_date

        task.updated_at = datetime.utcnow()
        return await self.task_repository.update(task)

    async def start_task(self, task_id: int) -> Task:
        """Start a task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        task.start_task()
        return await self.task_repository.update(task)

    async def complete_task(self, task_id: int) -> Task:
        """Complete a task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        task.complete_task()
        return await self.task_repository.update(task)

    async def log_time_on_task(self, task_id: int, hours: float) -> Task:
        """Log time worked on a task."""
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        task.update_progress(hours)
        return await self.task_repository.update(task)

    async def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        return await self.task_repository.delete(task_id)

    async def search_tasks(self, query: str, limit: int = 100, offset: int = 0) -> list[Task]:
        """Search tasks by title or description."""
        return await self.task_repository.search(query, limit=limit, offset=offset)

    async def get_overdue_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get overdue tasks."""
        return await self.task_repository.get_overdue_tasks(limit=limit, offset=offset)

    async def get_task_metrics(self, repository_id: int | None = None) -> dict:
        """Get task metrics and statistics."""
        return await self.task_repository.get_task_metrics(repository_id=repository_id)

    async def get_time_to_resolution_stats(self, repository_id: int | None = None) -> dict:
        """Get time-to-resolution statistics."""
        metrics = await self.task_repository.get_task_metrics(repository_id=repository_id)

        # Get completed tasks to calculate more detailed stats
        completed_tasks = await self.task_repository.get_by_status("completed", limit=1000)

        resolution_times = []
        for task in completed_tasks:
            if task.started_at and task.completed_at:
                resolution_time = task.get_time_to_resolution()
                if resolution_time:
                    resolution_times.append(resolution_time)

        if resolution_times:
            resolution_times.sort()
            count = len(resolution_times)
            median_index = count // 2

            return {
                "total_completed_tasks": count,
                "average_resolution_time_hours": sum(resolution_times) / count,
                "median_resolution_time_hours": resolution_times[median_index],
                "min_resolution_time_hours": min(resolution_times),
                "max_resolution_time_hours": max(resolution_times),
                "status_distribution": metrics.get("status_distribution", {}),
                "priority_distribution": metrics.get("priority_distribution", {}),
            }

        return {
            "total_completed_tasks": 0,
            "average_resolution_time_hours": 0.0,
            "median_resolution_time_hours": 0.0,
            "min_resolution_time_hours": 0.0,
            "max_resolution_time_hours": 0.0,
            "status_distribution": metrics.get("status_distribution", {}),
            "priority_distribution": metrics.get("priority_distribution", {}),
        }
