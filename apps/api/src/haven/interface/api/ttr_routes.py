"""TTR API routes for task management."""


from fastapi import APIRouter, Depends, HTTPException, Query, status

from haven.application.dtos.task_dtos import (
    TaskCreateRequest,
    TaskListResponse,
    TaskMetricsResponse,
    TaskResponse,
    TaskSearchRequest,
    TaskTimeLogRequest,
    TaskUpdateRequest,
    TimeToResolutionStatsResponse,
)
from haven.application.services.task_service import TaskService
from haven.domain.entities.task import Task
from haven.domain.unit_of_work import UnitOfWork
from haven.infrastructure.database.factory import db_factory
from haven.infrastructure.database.repositories.task_repository import TaskRepositoryImpl

router = APIRouter(prefix="/api/v1/ttr", tags=["TTR System"])


async def get_unit_of_work() -> UnitOfWork:
    """Dependency to get unit of work."""
    async for uow in db_factory.get_unit_of_work():
        yield uow


async def get_task_service(uow: UnitOfWork = Depends(get_unit_of_work)) -> TaskService:
    """Dependency to get task service."""
    task_repo = TaskRepositoryImpl(uow.session)
    return TaskService(task_repo)


def task_to_response(task: Task) -> TaskResponse:
    """Convert domain entity to response DTO."""
    return TaskResponse(
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


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Create a new task."""
    try:
        task = await service.create_task(
            title=request.title,
            description=request.description,
            priority=request.priority,
            task_type=request.task_type,
            assignee_id=request.assignee_id,
            repository_id=request.repository_id,
            estimated_hours=request.estimated_hours,
            due_date=request.due_date,
        )
        return task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    status_filter: str | None = Query(None, description="Filter by task status"),
    assignee_id: int | None = Query(None, description="Filter by assignee ID"),
    repository_id: int | None = Query(None, description="Filter by repository ID"),
    service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    """Get tasks with optional filters."""
    try:
        if status_filter:
            tasks = await service.get_tasks_by_status(status_filter, limit=limit, offset=offset)
        elif assignee_id:
            tasks = await service.get_tasks_by_assignee(assignee_id, limit=limit, offset=offset)
        elif repository_id:
            tasks = await service.get_tasks_by_repository(repository_id, limit=limit, offset=offset)
        else:
            tasks = await service.get_all_tasks(limit=limit, offset=offset)

        return TaskListResponse(
            tasks=[task_to_response(task) for task in tasks],
            total=len(tasks),
            offset=offset,
            limit=limit,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Get a specific task by ID."""
    task = await service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task_to_response(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Update a task."""
    try:
        task = await service.update_task(
            task_id=task_id,
            title=request.title,
            description=request.description,
            status=request.status,
            priority=request.priority,
            task_type=request.task_type,
            assignee_id=request.assignee_id,
            repository_id=request.repository_id,
            estimated_hours=request.estimated_hours,
            actual_hours=request.actual_hours,
            due_date=request.due_date,
        )
        return task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Delete a task."""
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("/tasks/search", response_model=TaskListResponse)
async def search_tasks(
    request: TaskSearchRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    """Search tasks by title or description."""
    try:
        tasks = await service.search_tasks(
            query=request.query,
            limit=request.limit,
            offset=request.offset,
        )

        return TaskListResponse(
            tasks=[task_to_response(task) for task in tasks],
            total=len(tasks),
            offset=request.offset,
            limit=request.limit,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/tasks/{task_id}/start", response_model=TaskResponse)
async def start_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Start working on a task."""
    try:
        task = await service.start_task(task_id)
        return task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Mark a task as completed."""
    try:
        task = await service.complete_task(task_id)
        return task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/tasks/{task_id}/log-time", response_model=TaskResponse)
async def log_time_on_task(
    task_id: int,
    request: TaskTimeLogRequest,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Log time worked on a task."""
    try:
        task = await service.log_time_on_task(task_id, request.hours)
        return task_to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/tasks/overdue", response_model=TaskListResponse)
async def get_overdue_tasks(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    service: TaskService = Depends(get_task_service),
) -> TaskListResponse:
    """Get overdue tasks."""
    try:
        tasks = await service.get_overdue_tasks(limit=limit, offset=offset)

        return TaskListResponse(
            tasks=[task_to_response(task) for task in tasks],
            total=len(tasks),
            offset=offset,
            limit=limit,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/metrics", response_model=TaskMetricsResponse)
async def get_task_metrics(
    repository_id: int | None = Query(None, description="Filter metrics by repository ID"),
    service: TaskService = Depends(get_task_service),
) -> TaskMetricsResponse:
    """Get task metrics and statistics."""
    try:
        metrics = await service.get_task_metrics(repository_id=repository_id)

        return TaskMetricsResponse(
            status_distribution=metrics.get("status_distribution", {}),
            priority_distribution=metrics.get("priority_distribution", {}),
            average_resolution_time_hours=metrics.get("average_resolution_time_hours", 0.0),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/ttr-stats", response_model=TimeToResolutionStatsResponse)
async def get_ttr_statistics(
    repository_id: int | None = Query(None, description="Filter stats by repository ID"),
    service: TaskService = Depends(get_task_service),
) -> TimeToResolutionStatsResponse:
    """Get time-to-resolution statistics."""
    try:
        stats = await service.get_time_to_resolution_stats(repository_id=repository_id)

        return TimeToResolutionStatsResponse(
            total_completed_tasks=stats["total_completed_tasks"],
            average_resolution_time_hours=stats["average_resolution_time_hours"],
            median_resolution_time_hours=stats["median_resolution_time_hours"],
            min_resolution_time_hours=stats["min_resolution_time_hours"],
            max_resolution_time_hours=stats["max_resolution_time_hours"],
            status_distribution=stats["status_distribution"],
            priority_distribution=stats["priority_distribution"],
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
