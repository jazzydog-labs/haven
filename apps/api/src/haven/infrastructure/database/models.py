"""SQLAlchemy models for database persistence."""

from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    type_annotation_map: ClassVar[dict[type, Any]] = {
        UUID: PostgresUUID(as_uuid=True),
        dict[str, Any]: JSON,
    }


__all__ = ["Base", "CommentModel", "MilestoneModel", "RecordModel", "RepositoryModel", "RoadmapModel", "TaskModel", "TimeLogModel", "TodoModel", "UserModel", "CommitModel", "CommitReviewModel", "ReviewCommentModel"]


class RecordModel(Base):
    """SQLAlchemy model for Record entity."""

    __tablename__ = "records"

    # Use String for SQLite testing, PostgresUUID for production
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of RecordModel."""
        return f"<RecordModel(id={self.id}, created_at={self.created_at})>"


class UserModel(Base):
    """SQLAlchemy model for User entity."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of UserModel."""
        return f"<UserModel(id={self.id}, username={self.username}, email={self.email})>"


class RepositoryModel(Base):
    """SQLAlchemy model for Repository entity."""

    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    branch: Mapped[str] = mapped_column(String(255), nullable=False, default="main")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_local: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of RepositoryModel."""
        return f"<RepositoryModel(id={self.id}, name={self.name}, url={self.url})>"


class TaskModel(Base):
    """SQLAlchemy model for Task entity."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open", index=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium", index=True)
    task_type: Mapped[str] = mapped_column(String(50), nullable=False, default="task", index=True)

    # Relationships
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    repository_id: Mapped[int | None] = mapped_column(ForeignKey("repositories.id"), nullable=True, index=True)

    # Time tracking
    estimated_hours: Mapped[float | None] = mapped_column(nullable=True)
    actual_hours: Mapped[float | None] = mapped_column(nullable=True)

    # Dates
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of TaskModel."""
        return f"<TaskModel(id={self.id}, title={self.title[:50]}, status={self.status})>"


class CommentModel(Base):
    """SQLAlchemy model for Comment entity."""

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    comment_type: Mapped[str] = mapped_column(String(50), nullable=False, default="comment", index=True)

    # Relationships
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Metadata
    comment_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of CommentModel."""
        return f"<CommentModel(id={self.id}, task_id={self.task_id}, author_id={self.author_id})>"


class TimeLogModel(Base):
    """SQLAlchemy model for TimeLog entity."""

    __tablename__ = "time_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    hours: Mapped[float] = mapped_column(nullable=False)
    log_type: Mapped[str] = mapped_column(String(50), nullable=False, default="work", index=True)

    # Relationships
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Date tracking
    logged_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of TimeLogModel."""
        return f"<TimeLogModel(id={self.id}, task_id={self.task_id}, hours={self.hours})>"


class TodoModel(Base):
    """SQLAlchemy model for Todo entity."""

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium", index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="general", index=True)

    # Relationships
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True, index=True)
    milestone_id: Mapped[int | None] = mapped_column(ForeignKey("milestones.id"), nullable=True, index=True)

    # Dates
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Metadata
    tags: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of TodoModel."""
        return f"<TodoModel(id={self.id}, title={self.title[:50]}, is_completed={self.is_completed})>"


class RoadmapModel(Base):
    """SQLAlchemy model for Roadmap entity."""

    __tablename__ = "roadmaps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    vision: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planning", index=True)

    # Relationships
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    repository_id: Mapped[int | None] = mapped_column(ForeignKey("repositories.id"), nullable=True, index=True)

    # Dates
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Metadata
    roadmap_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of RoadmapModel."""
        return f"<RoadmapModel(id={self.id}, name={self.name}, status={self.status})>"


class MilestoneModel(Base):
    """SQLAlchemy model for Milestone entity."""

    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="not_started", index=True)
    progress_percentage: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    roadmap_id: Mapped[int] = mapped_column(ForeignKey("roadmaps.id"), nullable=False, index=True)

    # Dates
    target_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Metrics
    estimated_effort_hours: Mapped[float | None] = mapped_column(nullable=True)
    actual_effort_hours: Mapped[float | None] = mapped_column(nullable=True)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of MilestoneModel."""
        return f"<MilestoneModel(id={self.id}, title={self.title[:50]}, progress={self.progress_percentage}%)>"


class CommitModel(Base):
    """SQLAlchemy model for Commit entity."""

    __tablename__ = "commits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), nullable=False, index=True)
    commit_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    author_name: Mapped[str] = mapped_column(String(255), nullable=False)
    author_email: Mapped[str] = mapped_column(String(255), nullable=False)
    committer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    committer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    committed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Diff statistics
    files_changed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    insertions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    deletions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Add unique constraint on repository_id + commit_hash
    __table_args__ = (
        UniqueConstraint('repository_id', 'commit_hash', name='_repository_commit_hash_uc'),
    )

    def __repr__(self) -> str:
        """String representation of CommitModel."""
        return f"<CommitModel(id={self.id}, hash={self.commit_hash[:7]}, message={self.message[:50]})>"


class CommitReviewModel(Base):
    """SQLAlchemy model for CommitReview entity."""

    __tablename__ = "commit_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    commit_id: Mapped[int] = mapped_column(ForeignKey("commits.id"), nullable=False, index=True)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_review", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of CommitReviewModel."""
        return f"<CommitReviewModel(id={self.id}, commit_id={self.commit_id}, status={self.status})>"


class ReviewCommentModel(Base):
    """SQLAlchemy model for ReviewComment entity."""

    __tablename__ = "review_comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    commit_id: Mapped[int] = mapped_column(ForeignKey("commits.id"), nullable=False, index=True)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    line_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """String representation of ReviewCommentModel."""
        comment_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<ReviewCommentModel(id={self.id}, commit_id={self.commit_id}, content='{comment_preview}')>"
