"""Task DTOs for the TTR system."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    """Request DTO for creating a task."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=5000, description="Task description")
    priority: str = Field("medium", description="Task priority (low, medium, high, urgent)")
    task_type: str = Field("task", description="Task type (task, todo, review, bug, feature)")
    assignee_id: Optional[int] = Field(None, description="ID of the assigned user")
    repository_id: Optional[int] = Field(None, description="ID of the associated repository")
    estimated_hours: Optional[float] = Field(None, ge=0, description="Estimated hours to complete")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")


class TaskUpdateRequest(BaseModel):
    """Request DTO for updating a task."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=5000, description="Task description")
    status: Optional[str] = Field(None, description="Task status (open, in_progress, completed, cancelled, blocked)")
    priority: Optional[str] = Field(None, description="Task priority (low, medium, high, urgent)")
    task_type: Optional[str] = Field(None, description="Task type (task, todo, review, bug, feature)")
    assignee_id: Optional[int] = Field(None, description="ID of the assigned user")
    repository_id: Optional[int] = Field(None, description="ID of the associated repository")
    estimated_hours: Optional[float] = Field(None, ge=0, description="Estimated hours to complete")
    actual_hours: Optional[float] = Field(None, ge=0, description="Actual hours spent")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")


class TaskResponse(BaseModel):
    """Response DTO for task data."""
    
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    task_type: str
    assignee_id: Optional[int]
    repository_id: Optional[int]
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    due_date: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    time_to_resolution: Optional[float]
    is_overdue: bool
    progress_percentage: float


class TaskListResponse(BaseModel):
    """Response DTO for task list."""
    
    tasks: list[TaskResponse]
    total: int
    offset: int
    limit: int


class TaskMetricsResponse(BaseModel):
    """Response DTO for task metrics."""
    
    status_distribution: dict[str, int]
    priority_distribution: dict[str, int]
    average_resolution_time_hours: float


class TimeToResolutionStatsResponse(BaseModel):
    """Response DTO for time-to-resolution statistics."""
    
    total_completed_tasks: int
    average_resolution_time_hours: float
    median_resolution_time_hours: float
    min_resolution_time_hours: float
    max_resolution_time_hours: float
    status_distribution: dict[str, int]
    priority_distribution: dict[str, int]


class TaskSearchRequest(BaseModel):
    """Request DTO for searching tasks."""
    
    query: str = Field(..., min_length=1, description="Search query")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of results")
    offset: int = Field(0, ge=0, description="Offset for pagination")


class TaskStatusUpdateRequest(BaseModel):
    """Request DTO for updating task status."""
    
    status: str = Field(..., description="New task status (open, in_progress, completed, cancelled, blocked)")


class TaskTimeLogRequest(BaseModel):
    """Request DTO for logging time on a task."""
    
    hours: float = Field(..., ge=0, le=24, description="Hours worked on the task")