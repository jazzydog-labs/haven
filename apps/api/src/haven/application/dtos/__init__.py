"""Application DTOs (Data Transfer Objects)."""

from haven.application.dtos.record_dtos import (
    RecordCreateDTO,
    RecordResponseDTO,
    RecordUpdateDTO,
)
from haven.application.dtos.task_dtos import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse,
    TaskMetricsResponse,
    TimeToResolutionStatsResponse,
    TaskSearchRequest,
    TaskStatusUpdateRequest,
    TaskTimeLogRequest,
)

__all__ = [
    "RecordCreateDTO",
    "RecordResponseDTO", 
    "RecordUpdateDTO",
    "TaskCreateRequest",
    "TaskUpdateRequest",
    "TaskResponse",
    "TaskListResponse",
    "TaskMetricsResponse",
    "TimeToResolutionStatsResponse",
    "TaskSearchRequest",
    "TaskStatusUpdateRequest",
    "TaskTimeLogRequest",
]
