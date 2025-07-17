"""Comment repository implementation using SQLAlchemy."""

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.comment import Comment
from haven.domain.repositories.comment_repository import CommentRepository
from haven.infrastructure.database.models import CommentModel


class CommentRepositoryImpl(CommentRepository):
    """SQLAlchemy implementation of CommentRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, comment: Comment) -> Comment:
        """Create a new comment."""
        comment_model = CommentModel(
            content=comment.content,
            comment_type=comment.comment_type,
            task_id=comment.task_id,
            author_id=comment.author_id,
            comment_metadata=comment.metadata,
        )

        self.session.add(comment_model)
        await self.session.flush()

        return self._model_to_entity(comment_model)

    async def get_by_id(self, comment_id: int) -> Comment | None:
        """Get a comment by its ID."""
        result = await self.session.get(CommentModel, comment_id)
        return self._model_to_entity(result) if result else None

    async def get_by_task(self, task_id: int, limit: int = 100, offset: int = 0) -> list[Comment]:
        """Get comments for a specific task."""
        result = await self.session.execute(
            CommentModel.__table__.select()
            .where(CommentModel.task_id == task_id)
            .order_by(desc(CommentModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(CommentModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_author(
        self, author_id: int, limit: int = 100, offset: int = 0
    ) -> list[Comment]:
        """Get comments by author."""
        result = await self.session.execute(
            CommentModel.__table__.select()
            .where(CommentModel.author_id == author_id)
            .order_by(desc(CommentModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(CommentModel(**row._mapping)) for row in result.fetchall()]

    async def get_by_type(
        self, comment_type: str, limit: int = 100, offset: int = 0
    ) -> list[Comment]:
        """Get comments by type."""
        result = await self.session.execute(
            CommentModel.__table__.select()
            .where(CommentModel.comment_type == comment_type)
            .order_by(desc(CommentModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(CommentModel(**row._mapping)) for row in result.fetchall()]

    async def update(self, comment: Comment) -> Comment:
        """Update an existing comment."""
        comment_model = await self.session.get(CommentModel, comment.id)
        if not comment_model:
            raise ValueError(f"Comment with ID {comment.id} not found")

        comment_model.content = comment.content
        comment_model.comment_type = comment.comment_type
        comment_model.comment_metadata = comment.metadata
        comment_model.updated_at = comment.updated_at

        await self.session.flush()
        return self._model_to_entity(comment_model)

    async def delete(self, comment_id: int) -> bool:
        """Delete a comment by its ID."""
        comment_model = await self.session.get(CommentModel, comment_id)
        if not comment_model:
            return False

        await self.session.delete(comment_model)
        await self.session.flush()
        return True

    async def get_recent_comments(self, limit: int = 10) -> list[Comment]:
        """Get recent comments across all tasks."""
        result = await self.session.execute(
            CommentModel.__table__.select().order_by(desc(CommentModel.created_at)).limit(limit)
        )
        return [self._model_to_entity(CommentModel(**row._mapping)) for row in result.fetchall()]

    async def search(self, query: str, limit: int = 100, offset: int = 0) -> list[Comment]:
        """Search comments by content."""
        result = await self.session.execute(
            CommentModel.__table__.select()
            .where(CommentModel.content.ilike(f"%{query}%"))
            .order_by(desc(CommentModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [self._model_to_entity(CommentModel(**row._mapping)) for row in result.fetchall()]

    def _model_to_entity(self, model: CommentModel) -> Comment:
        """Convert CommentModel to Comment entity."""
        return Comment(
            id=model.id,
            content=model.content,
            comment_type=model.comment_type,
            task_id=model.task_id,
            author_id=model.author_id,
            metadata=model.comment_metadata,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
