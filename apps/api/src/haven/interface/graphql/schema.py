"""GraphQL schema definition."""

from datetime import datetime
from uuid import UUID

import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info

from haven.application.services import RecordService
from haven.application.services.task_service import TaskService
from haven.domain.entities import Record
from haven.domain.entities.task import Task
from haven.infrastructure.database.factory import db_factory
from haven.infrastructure.database.repositories.task_repository import TaskRepositoryImpl


@strawberry.type
class RecordType:
    """GraphQL type for Record."""

    id: UUID
    data: JSON
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, record: Record) -> "RecordType":
        """Create GraphQL type from domain entity."""
        return cls(
            id=record.id,
            data=record.data,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


@strawberry.type
class RecordConnection:
    """Relay-style connection for records."""

    edges: list["RecordEdge"]
    page_info: "PageInfo"


@strawberry.type
class RecordEdge:
    """Edge in record connection."""

    cursor: str
    node: RecordType


@strawberry.type
class PageInfo:
    """Page information for pagination."""

    has_next_page: bool
    end_cursor: str | None


@strawberry.input
class RecordInput:
    """Input type for creating/updating records."""

    data: JSON


@strawberry.type
class TaskType:
    """GraphQL type for Task."""

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    task_type: str
    assignee_id: int | None
    repository_id: int | None
    estimated_hours: float | None
    actual_hours: float | None
    due_date: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    time_to_resolution: float | None
    is_overdue: bool
    progress_percentage: float

    @classmethod
    def from_entity(cls, task: Task) -> "TaskType":
        """Create GraphQL type from domain entity."""
        return cls(
            id=task.id,
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
            created_at=task.created_at,
            updated_at=task.updated_at,
            time_to_resolution=task.get_time_to_resolution(),
            is_overdue=task.is_overdue(),
            progress_percentage=task.get_progress_percentage(),
        )


@strawberry.type
class TaskConnection:
    """Relay-style connection for tasks."""

    edges: list["TaskEdge"]
    page_info: "PageInfo"


@strawberry.type
class TaskEdge:
    """Edge in task connection."""

    cursor: str
    node: TaskType


@strawberry.type
class TaskMetrics:
    """GraphQL type for task metrics."""

    status_distribution: JSON
    priority_distribution: JSON
    average_resolution_time_hours: float


@strawberry.type
class TimeToResolutionStats:
    """GraphQL type for time-to-resolution statistics."""

    total_completed_tasks: int
    average_resolution_time_hours: float
    median_resolution_time_hours: float
    min_resolution_time_hours: float
    max_resolution_time_hours: float
    status_distribution: JSON
    priority_distribution: JSON


@strawberry.input
class TaskInput:
    """Input type for creating tasks."""

    title: str
    description: str | None = None
    priority: str = "medium"
    task_type: str = "task"
    assignee_id: int | None = None
    repository_id: int | None = None
    estimated_hours: float | None = None
    due_date: datetime | None = None


@strawberry.input
class TaskUpdateInput:
    """Input type for updating tasks."""

    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    task_type: str | None = None
    assignee_id: int | None = None
    repository_id: int | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    due_date: datetime | None = None


@strawberry.type
class Query:
    """Root query type."""

    @strawberry.field
    async def record(self, info: Info, id: UUID) -> RecordType | None:
        """Get a single record by ID."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                service = RecordService(uow)
                try:
                    record = await service.get_record(id)
                    return RecordType.from_entity(record)
                except Exception:
                    return None

    @strawberry.field
    async def records(
        self,
        info: Info,
        first: int = 25,
        after: str | None = None,
    ) -> RecordConnection:
        """List records with cursor-based pagination."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                service = RecordService(uow)

                # Decode cursor to offset
                offset = 0
                if after:
                    try:
                        offset = int(after)
                    except ValueError:
                        offset = 0

                # Get records
                records, total = await service.list_records(limit=first + 1, offset=offset)

                # Check if there are more records
                has_next = len(records) > first
                if has_next:
                    records = records[:first]

                # Create edges
                edges = []
                for i, record in enumerate(records):
                    cursor = str(offset + i)
                    edges.append(
                        RecordEdge(
                            cursor=cursor,
                            node=RecordType.from_entity(record),
                        )
                    )

                # Create page info
                end_cursor = edges[-1].cursor if edges else None
                page_info = PageInfo(
                    has_next_page=has_next,
                    end_cursor=end_cursor,
                )

                return RecordConnection(edges=edges, page_info=page_info)

    @strawberry.field
    async def task(self, info: Info, id: int) -> TaskType | None:
        """Get a single task by ID."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)
                task = await service.get_task_by_id(id)
                return TaskType.from_entity(task) if task else None

    @strawberry.field
    async def tasks(
        self,
        info: Info,
        first: int = 25,
        after: str | None = None,
        status: str | None = None,
        assignee_id: int | None = None,
        repository_id: int | None = None,
    ) -> TaskConnection:
        """List tasks with optional filters and cursor-based pagination."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                # Decode cursor to offset
                offset = 0
                if after:
                    try:
                        offset = int(after)
                    except ValueError:
                        offset = 0

                # Get tasks with filters
                if status:
                    tasks = await service.get_tasks_by_status(
                        status, limit=first + 1, offset=offset
                    )
                elif assignee_id:
                    tasks = await service.get_tasks_by_assignee(
                        assignee_id, limit=first + 1, offset=offset
                    )
                elif repository_id:
                    tasks = await service.get_tasks_by_repository(
                        repository_id, limit=first + 1, offset=offset
                    )
                else:
                    tasks = await service.get_all_tasks(limit=first + 1, offset=offset)

                # Check if there are more tasks
                has_next = len(tasks) > first
                if has_next:
                    tasks = tasks[:first]

                # Create edges
                edges = []
                for i, task in enumerate(tasks):
                    cursor = str(offset + i)
                    edges.append(
                        TaskEdge(
                            cursor=cursor,
                            node=TaskType.from_entity(task),
                        )
                    )

                # Create page info
                end_cursor = edges[-1].cursor if edges else None
                page_info = PageInfo(
                    has_next_page=has_next,
                    end_cursor=end_cursor,
                )

                return TaskConnection(edges=edges, page_info=page_info)

    @strawberry.field
    async def overdue_tasks(
        self,
        info: Info,
        first: int = 25,
        after: str | None = None,
    ) -> TaskConnection:
        """List overdue tasks with cursor-based pagination."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                # Decode cursor to offset
                offset = 0
                if after:
                    try:
                        offset = int(after)
                    except ValueError:
                        offset = 0

                # Get overdue tasks
                tasks = await service.get_overdue_tasks(limit=first + 1, offset=offset)

                # Check if there are more tasks
                has_next = len(tasks) > first
                if has_next:
                    tasks = tasks[:first]

                # Create edges
                edges = []
                for i, task in enumerate(tasks):
                    cursor = str(offset + i)
                    edges.append(
                        TaskEdge(
                            cursor=cursor,
                            node=TaskType.from_entity(task),
                        )
                    )

                # Create page info
                end_cursor = edges[-1].cursor if edges else None
                page_info = PageInfo(
                    has_next_page=has_next,
                    end_cursor=end_cursor,
                )

                return TaskConnection(edges=edges, page_info=page_info)

    @strawberry.field
    async def search_tasks(
        self,
        info: Info,
        query: str,
        first: int = 25,
        after: str | None = None,
    ) -> TaskConnection:
        """Search tasks by title or description."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                # Decode cursor to offset
                offset = 0
                if after:
                    try:
                        offset = int(after)
                    except ValueError:
                        offset = 0

                # Search tasks
                tasks = await service.search_tasks(query, limit=first + 1, offset=offset)

                # Check if there are more tasks
                has_next = len(tasks) > first
                if has_next:
                    tasks = tasks[:first]

                # Create edges
                edges = []
                for i, task in enumerate(tasks):
                    cursor = str(offset + i)
                    edges.append(
                        TaskEdge(
                            cursor=cursor,
                            node=TaskType.from_entity(task),
                        )
                    )

                # Create page info
                end_cursor = edges[-1].cursor if edges else None
                page_info = PageInfo(
                    has_next_page=has_next,
                    end_cursor=end_cursor,
                )

                return TaskConnection(edges=edges, page_info=page_info)

    @strawberry.field
    async def task_metrics(
        self,
        info: Info,
        repository_id: int | None = None,
    ) -> TaskMetrics:
        """Get task metrics and statistics."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                metrics = await service.get_task_metrics(repository_id=repository_id)

                return TaskMetrics(
                    status_distribution=metrics.get("status_distribution", {}),
                    priority_distribution=metrics.get("priority_distribution", {}),
                    average_resolution_time_hours=metrics.get("average_resolution_time_hours", 0.0),
                )

    @strawberry.field
    async def ttr_stats(
        self,
        info: Info,
        repository_id: int | None = None,
    ) -> TimeToResolutionStats:
        """Get time-to-resolution statistics."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                stats = await service.get_time_to_resolution_stats(repository_id=repository_id)

                return TimeToResolutionStats(
                    total_completed_tasks=stats["total_completed_tasks"],
                    average_resolution_time_hours=stats["average_resolution_time_hours"],
                    median_resolution_time_hours=stats["median_resolution_time_hours"],
                    min_resolution_time_hours=stats["min_resolution_time_hours"],
                    max_resolution_time_hours=stats["max_resolution_time_hours"],
                    status_distribution=stats["status_distribution"],
                    priority_distribution=stats["priority_distribution"],
                )


@strawberry.type
class Mutation:
    """Root mutation type."""

    @strawberry.mutation
    async def create_record(self, info: Info, input: RecordInput) -> RecordType:
        """Create a new record."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                service = RecordService(uow)
                record = await service.create_record(input.data)
                return RecordType.from_entity(record)

    @strawberry.mutation
    async def update_record(self, info: Info, id: UUID, input: RecordInput) -> RecordType:
        """Update an existing record."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                service = RecordService(uow)
                record = await service.update_record(id, input.data)
                return RecordType.from_entity(record)

    @strawberry.mutation
    async def delete_record(self, info: Info, id: UUID) -> bool:
        """Delete a record by ID."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                service = RecordService(uow)
                return await service.delete_record(id)

    @strawberry.mutation
    async def create_task(self, info: Info, input: TaskInput) -> TaskType:
        """Create a new task."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                task = await service.create_task(
                    title=input.title,
                    description=input.description,
                    priority=input.priority,
                    task_type=input.task_type,
                    assignee_id=input.assignee_id,
                    repository_id=input.repository_id,
                    estimated_hours=input.estimated_hours,
                    due_date=input.due_date,
                )

                return TaskType.from_entity(task)

    @strawberry.mutation
    async def update_task(self, info: Info, id: int, input: TaskUpdateInput) -> TaskType:
        """Update an existing task."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                task = await service.update_task(
                    task_id=id,
                    title=input.title,
                    description=input.description,
                    status=input.status,
                    priority=input.priority,
                    task_type=input.task_type,
                    assignee_id=input.assignee_id,
                    repository_id=input.repository_id,
                    estimated_hours=input.estimated_hours,
                    actual_hours=input.actual_hours,
                    due_date=input.due_date,
                )

                return TaskType.from_entity(task)

    @strawberry.mutation
    async def delete_task(self, info: Info, id: int) -> bool:
        """Delete a task by ID."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)
                return await service.delete_task(id)

    @strawberry.mutation
    async def start_task(self, info: Info, id: int) -> TaskType:
        """Start working on a task."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                task = await service.start_task(id)
                return TaskType.from_entity(task)

    @strawberry.mutation
    async def complete_task(self, info: Info, id: int) -> TaskType:
        """Mark a task as completed."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                task = await service.complete_task(id)
                return TaskType.from_entity(task)

    @strawberry.mutation
    async def log_time_on_task(self, info: Info, id: int, hours: float) -> TaskType:
        """Log time worked on a task."""
        async for uow in db_factory.get_unit_of_work():
            async with uow:
                task_repo = TaskRepositoryImpl(uow.session)
                service = TaskService(task_repo)

                task = await service.log_time_on_task(id, hours)
                return TaskType.from_entity(task)


# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
