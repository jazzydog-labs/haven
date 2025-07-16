"""TimeLog repository implementation using SQLAlchemy."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.time_log import TimeLog
from haven.domain.repositories.time_log_repository import TimeLogRepository
from haven.infrastructure.database.models import TimeLogModel


class TimeLogRepositoryImpl(TimeLogRepository):
    """SQLAlchemy implementation of TimeLogRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, time_log: TimeLog) -> TimeLog:
        """Create a new time log."""
        time_log_model = TimeLogModel(
            description=time_log.description,
            hours=time_log.hours,
            log_type=time_log.log_type,
            task_id=time_log.task_id,
            user_id=time_log.user_id,
            logged_date=time_log.logged_date,
        )
        
        self.session.add(time_log_model)
        await self.session.flush()
        
        return self._model_to_entity(time_log_model)

    async def get_by_id(self, time_log_id: int) -> Optional[TimeLog]:
        """Get a time log by its ID."""
        result = await self.session.get(TimeLogModel, time_log_id)
        return self._model_to_entity(result) if result else None

    async def get_by_task(self, task_id: int, limit: int = 100, offset: int = 0) -> List[TimeLog]:
        """Get time logs for a specific task."""
        result = await self.session.execute(
            TimeLogModel.__table__.select()
            .where(TimeLogModel.task_id == task_id)
            .order_by(desc(TimeLogModel.logged_date))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TimeLogModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_user(self, user_id: int, limit: int = 100, offset: int = 0) -> List[TimeLog]:
        """Get time logs by user."""
        result = await self.session.execute(
            TimeLogModel.__table__.select()
            .where(TimeLogModel.user_id == user_id)
            .order_by(desc(TimeLogModel.logged_date))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TimeLogModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        user_id: Optional[int] = None,
        limit: int = 100, 
        offset: int = 0
    ) -> List[TimeLog]:
        """Get time logs within a date range."""
        query = TimeLogModel.__table__.select().where(
            and_(
                TimeLogModel.logged_date >= start_date,
                TimeLogModel.logged_date <= end_date
            )
        )
        
        if user_id:
            query = query.where(TimeLogModel.user_id == user_id)
        
        result = await self.session.execute(
            query.order_by(desc(TimeLogModel.logged_date))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TimeLogModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_type(self, log_type: str, limit: int = 100, offset: int = 0) -> List[TimeLog]:
        """Get time logs by type."""
        result = await self.session.execute(
            TimeLogModel.__table__.select()
            .where(TimeLogModel.log_type == log_type)
            .order_by(desc(TimeLogModel.logged_date))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(TimeLogModel(**row._mapping)) for row in result.fetchall()]

    async def update(self, time_log: TimeLog) -> TimeLog:
        """Update an existing time log."""
        time_log_model = await self.session.get(TimeLogModel, time_log.id)
        if not time_log_model:
            raise ValueError(f"TimeLog with ID {time_log.id} not found")

        time_log_model.description = time_log.description
        time_log_model.hours = time_log.hours
        time_log_model.log_type = time_log.log_type
        time_log_model.logged_date = time_log.logged_date
        time_log_model.updated_at = time_log.updated_at

        await self.session.flush()
        return self._model_to_entity(time_log_model)

    async def delete(self, time_log_id: int) -> bool:
        """Delete a time log by its ID."""
        time_log_model = await self.session.get(TimeLogModel, time_log_id)
        if not time_log_model:
            return False

        await self.session.delete(time_log_model)
        await self.session.flush()
        return True

    async def get_total_hours_by_task(self, task_id: int) -> float:
        """Get total hours logged for a specific task."""
        result = await self.session.execute(
            func.sum(TimeLogModel.hours).where(TimeLogModel.task_id == task_id)
        )
        return result.scalar() or 0.0

    async def get_total_hours_by_user(self, user_id: int, start_date: datetime, end_date: datetime) -> float:
        """Get total hours logged by a user within a date range."""
        result = await self.session.execute(
            func.sum(TimeLogModel.hours).where(
                and_(
                    TimeLogModel.user_id == user_id,
                    TimeLogModel.logged_date >= start_date,
                    TimeLogModel.logged_date <= end_date
                )
            )
        )
        return result.scalar() or 0.0

    async def get_daily_summary(self, user_id: int, date: datetime) -> dict:
        """Get daily time log summary for a user."""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Total hours by type
        type_summary = await self.session.execute(
            TimeLogModel.__table__.select()
            .with_only_columns(
                TimeLogModel.log_type,
                func.sum(TimeLogModel.hours).label("total_hours")
            )
            .where(
                and_(
                    TimeLogModel.user_id == user_id,
                    TimeLogModel.logged_date >= start_of_day,
                    TimeLogModel.logged_date <= end_of_day
                )
            )
            .group_by(TimeLogModel.log_type)
        )
        
        # Total hours
        total_hours = await self.session.execute(
            func.sum(TimeLogModel.hours).where(
                and_(
                    TimeLogModel.user_id == user_id,
                    TimeLogModel.logged_date >= start_of_day,
                    TimeLogModel.logged_date <= end_of_day
                )
            )
        )
        
        return {
            "date": date.date().isoformat(),
            "total_hours": total_hours.scalar() or 0.0,
            "hours_by_type": {row.log_type: row.total_hours for row in type_summary.fetchall()},
        }

    async def get_weekly_summary(self, user_id: int, start_date: datetime) -> dict:
        """Get weekly time log summary for a user."""
        end_date = start_date + datetime.timedelta(days=7)
        
        # Total hours by day
        daily_summary = await self.session.execute(
            TimeLogModel.__table__.select()
            .with_only_columns(
                func.date(TimeLogModel.logged_date).label("date"),
                func.sum(TimeLogModel.hours).label("total_hours")
            )
            .where(
                and_(
                    TimeLogModel.user_id == user_id,
                    TimeLogModel.logged_date >= start_date,
                    TimeLogModel.logged_date < end_date
                )
            )
            .group_by(func.date(TimeLogModel.logged_date))
        )
        
        # Total hours by type
        type_summary = await self.session.execute(
            TimeLogModel.__table__.select()
            .with_only_columns(
                TimeLogModel.log_type,
                func.sum(TimeLogModel.hours).label("total_hours")
            )
            .where(
                and_(
                    TimeLogModel.user_id == user_id,
                    TimeLogModel.logged_date >= start_date,
                    TimeLogModel.logged_date < end_date
                )
            )
            .group_by(TimeLogModel.log_type)
        )
        
        # Total hours
        total_hours = await self.session.execute(
            func.sum(TimeLogModel.hours).where(
                and_(
                    TimeLogModel.user_id == user_id,
                    TimeLogModel.logged_date >= start_date,
                    TimeLogModel.logged_date < end_date
                )
            )
        )
        
        return {
            "week_start": start_date.date().isoformat(),
            "week_end": end_date.date().isoformat(),
            "total_hours": total_hours.scalar() or 0.0,
            "hours_by_day": {str(row.date): row.total_hours for row in daily_summary.fetchall()},
            "hours_by_type": {row.log_type: row.total_hours for row in type_summary.fetchall()},
        }

    async def get_efficiency_metrics(self, user_id: Optional[int] = None) -> dict:
        """Get efficiency metrics and statistics."""
        base_query = TimeLogModel.__table__.select()
        if user_id:
            base_query = base_query.where(TimeLogModel.user_id == user_id)
        
        # Average hours by type
        avg_by_type = await self.session.execute(
            base_query.with_only_columns(
                TimeLogModel.log_type,
                func.avg(TimeLogModel.hours).label("avg_hours")
            ).group_by(TimeLogModel.log_type)
        )
        
        # Total efficiency score
        efficiency_query = base_query.with_only_columns(
            func.sum(
                func.case(
                    (TimeLogModel.log_type == "work", TimeLogModel.hours * 1.0),
                    (TimeLogModel.log_type == "review", TimeLogModel.hours * 0.8),
                    (TimeLogModel.log_type == "testing", TimeLogModel.hours * 0.9),
                    (TimeLogModel.log_type == "documentation", TimeLogModel.hours * 0.7),
                    (TimeLogModel.log_type == "meeting", TimeLogModel.hours * 0.5),
                    else_=TimeLogModel.hours * 1.0
                )
            ).label("efficiency_score")
        )
        
        efficiency_score = await self.session.execute(efficiency_query)
        
        return {
            "average_hours_by_type": {row.log_type: float(row.avg_hours) for row in avg_by_type.fetchall()},
            "total_efficiency_score": efficiency_score.scalar() or 0.0,
        }

    def _model_to_entity(self, model: TimeLogModel) -> TimeLog:
        """Convert TimeLogModel to TimeLog entity."""
        return TimeLog(
            id=model.id,
            description=model.description,
            hours=model.hours,
            log_type=model.log_type,
            task_id=model.task_id,
            user_id=model.user_id,
            logged_date=model.logged_date,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )