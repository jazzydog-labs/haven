"""Task repository implementation using SQLAlchemy."""

from datetime import datetime

from sqlalchemy import and_, desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.task import Task
from haven.domain.repositories.task_repository import TaskRepository
from haven.infrastructure.database.models import TaskModel


class TaskRepositoryImpl(TaskRepository):
    """SQLAlchemy implementation of TaskRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        """Create a new task."""
        task_model = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            task_type=task.task_type,
            assignee_id=task.assignee_id,
            repository_id=task.repository_id,
            estimated_hours=task.estimated_hours,
            actual_hours=task.actual_hours,
            due_date=task.due_date,
            started_at=task.started_at,
            completed_at=task.completed_at,
        )

        self.session.add(task_model)
        await self.session.flush()

        return self._model_to_entity(task_model)

    async def get_by_id(self, task_id: int) -> Task | None:
        """Get a task by its ID."""
        result = await self.session.get(TaskModel, task_id)
        return self._model_to_entity(result) if result else None

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get all tasks with pagination."""
        result = await self.session.execute(
            TaskModel.__table__.select()
            .order_by(desc(TaskModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TaskModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_status(self, status: str, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get tasks by status."""
        result = await self.session.execute(
            TaskModel.__table__.select()
            .where(TaskModel.status == status)
            .order_by(desc(TaskModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TaskModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_assignee(self, assignee_id: int, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get tasks by assignee."""
        result = await self.session.execute(
            TaskModel.__table__.select()
            .where(TaskModel.assignee_id == assignee_id)
            .order_by(desc(TaskModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TaskModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_repository(self, repository_id: int, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get tasks by repository."""
        result = await self.session.execute(
            TaskModel.__table__.select()
            .where(TaskModel.repository_id == repository_id)
            .order_by(desc(TaskModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TaskModel(**row._mapping)) for row in result.fetchall()]

    async def update(self, task: Task) -> Task:
        """Update an existing task."""
        task_model = await self.session.get(TaskModel, task.id)
        if not task_model:
            raise ValueError(f"Task with ID {task.id} not found")

        task_model.title = task.title
        task_model.description = task.description
        task_model.status = task.status
        task_model.priority = task.priority
        task_model.task_type = task.task_type
        task_model.assignee_id = task.assignee_id
        task_model.repository_id = task.repository_id
        task_model.estimated_hours = task.estimated_hours
        task_model.actual_hours = task.actual_hours
        task_model.due_date = task.due_date
        task_model.started_at = task.started_at
        task_model.completed_at = task.completed_at
        task_model.updated_at = task.updated_at

        await self.session.flush()
        return self._model_to_entity(task_model)

    async def delete(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        task_model = await self.session.get(TaskModel, task_id)
        if not task_model:
            return False

        await self.session.delete(task_model)
        await self.session.flush()
        return True

    async def search(self, query: str, limit: int = 100, offset: int = 0) -> list[Task]:
        """Search tasks by title or description."""
        result = await self.session.execute(
            TaskModel.__table__.select()
            .where(or_(
                TaskModel.title.ilike(f"%{query}%"),
                TaskModel.description.ilike(f"%{query}%")
            ))
            .order_by(desc(TaskModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TaskModel(**row._mapping)) for row in result.fetchall()]

    async def get_overdue_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        """Get overdue tasks."""
        now = datetime.utcnow()
        result = await self.session.execute(
            TaskModel.__table__.select()
            .where(and_(
                TaskModel.due_date < now,
                TaskModel.status != "completed"
            ))
            .order_by(TaskModel.due_date)
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TaskModel(**row._mapping)) for row in result.fetchall()]

    async def get_task_metrics(self, repository_id: int | None = None) -> dict:
        """Get task metrics and statistics."""
        base_query = TaskModel.__table__.select()
        if repository_id:
            base_query = base_query.where(TaskModel.repository_id == repository_id)

        # Count by status
        status_counts = await self.session.execute(
            base_query.with_only_columns(
                TaskModel.status,
                func.count(TaskModel.id).label("count")
            ).group_by(TaskModel.status)
        )

        # Count by priority
        priority_counts = await self.session.execute(
            base_query.with_only_columns(
                TaskModel.priority,
                func.count(TaskModel.id).label("count")
            ).group_by(TaskModel.priority)
        )

        # Average time to resolution
        avg_resolution_time = await self.session.execute(
            base_query.with_only_columns(
                func.avg(
                    func.extract('epoch', TaskModel.completed_at - TaskModel.started_at) / 3600
                ).label("avg_hours")
            ).where(and_(
                TaskModel.status == "completed",
                TaskModel.started_at.is_not(None),
                TaskModel.completed_at.is_not(None)
            ))
        )

        return {
            "status_distribution": {row.status: row.count for row in status_counts.fetchall()},
            "priority_distribution": {row.priority: row.count for row in priority_counts.fetchall()},
            "average_resolution_time_hours": avg_resolution_time.scalar() or 0.0,
        }

    def _model_to_entity(self, model: TaskModel) -> Task:
        """Convert TaskModel to Task entity."""
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            priority=model.priority,
            task_type=model.task_type,
            assignee_id=model.assignee_id,
            repository_id=model.repository_id,
            estimated_hours=model.estimated_hours,
            actual_hours=model.actual_hours,
            due_date=model.due_date,
            started_at=model.started_at,
            completed_at=model.completed_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
