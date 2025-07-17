"""TimeLog repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime

from haven.domain.entities.time_log import TimeLog


class TimeLogRepository(ABC):
    """Abstract repository for TimeLog entities."""

    @abstractmethod
    async def create(self, time_log: TimeLog) -> TimeLog:
        """Create a new time log."""
        pass

    @abstractmethod
    async def get_by_id(self, time_log_id: int) -> TimeLog | None:
        """Get a time log by its ID."""
        pass

    @abstractmethod
    async def get_by_task(self, task_id: int, limit: int = 100, offset: int = 0) -> list[TimeLog]:
        """Get time logs for a specific task."""
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int, limit: int = 100, offset: int = 0) -> list[TimeLog]:
        """Get time logs by user."""
        pass

    @abstractmethod
    async def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        user_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TimeLog]:
        """Get time logs within a date range."""
        pass

    @abstractmethod
    async def get_by_type(self, log_type: str, limit: int = 100, offset: int = 0) -> list[TimeLog]:
        """Get time logs by type."""
        pass

    @abstractmethod
    async def update(self, time_log: TimeLog) -> TimeLog:
        """Update an existing time log."""
        pass

    @abstractmethod
    async def delete(self, time_log_id: int) -> bool:
        """Delete a time log by its ID."""
        pass

    @abstractmethod
    async def get_total_hours_by_task(self, task_id: int) -> float:
        """Get total hours logged for a specific task."""
        pass

    @abstractmethod
    async def get_total_hours_by_user(
        self, user_id: int, start_date: datetime, end_date: datetime
    ) -> float:
        """Get total hours logged by a user within a date range."""
        pass

    @abstractmethod
    async def get_daily_summary(self, user_id: int, date: datetime) -> dict:
        """Get daily time log summary for a user."""
        pass

    @abstractmethod
    async def get_weekly_summary(self, user_id: int, start_date: datetime) -> dict:
        """Get weekly time log summary for a user."""
        pass

    @abstractmethod
    async def get_efficiency_metrics(self, user_id: int | None = None) -> dict:
        """Get efficiency metrics and statistics."""
        pass
