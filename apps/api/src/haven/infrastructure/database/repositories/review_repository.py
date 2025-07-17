"""SQLAlchemy implementation of review repositories."""

from sqlalchemy import and_, delete, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.review_comment import CommitReview, ReviewComment
from haven.domain.repositories.review_repository import (
    CommitReviewRepository,
    ReviewCommentRepository,
)
from haven.infrastructure.database.models import CommitReviewModel, ReviewCommentModel


class SqlAlchemyReviewCommentRepository(ReviewCommentRepository):
    """SQLAlchemy implementation of ReviewCommentRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, review_comment: ReviewComment) -> ReviewComment:
        """Create a new review comment."""
        model = ReviewCommentModel(
            commit_id=review_comment.commit_id,
            reviewer_id=review_comment.reviewer_id,
            line_number=review_comment.line_number,
            file_path=review_comment.file_path,
            content=review_comment.content,
            created_at=review_comment.created_at,
            updated_at=review_comment.updated_at,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def get_by_id(self, comment_id: int) -> ReviewComment | None:
        """Get a review comment by ID."""
        stmt = select(ReviewCommentModel).where(ReviewCommentModel.id == comment_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def get_by_commit_id(self, commit_id: int) -> list[ReviewComment]:
        """Get all review comments for a commit."""
        stmt = (
            select(ReviewCommentModel)
            .where(ReviewCommentModel.commit_id == commit_id)
            .order_by(
                ReviewCommentModel.file_path,
                ReviewCommentModel.line_number,
                ReviewCommentModel.created_at,
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_reviewer_id(self, reviewer_id: int) -> list[ReviewComment]:
        """Get all review comments by a specific reviewer."""
        stmt = (
            select(ReviewCommentModel)
            .where(ReviewCommentModel.reviewer_id == reviewer_id)
            .order_by(ReviewCommentModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_commit_and_reviewer(
        self, commit_id: int, reviewer_id: int
    ) -> list[ReviewComment]:
        """Get review comments for a commit by a specific reviewer."""
        stmt = (
            select(ReviewCommentModel)
            .where(
                and_(
                    ReviewCommentModel.commit_id == commit_id,
                    ReviewCommentModel.reviewer_id == reviewer_id,
                )
            )
            .order_by(
                ReviewCommentModel.file_path,
                ReviewCommentModel.line_number,
                ReviewCommentModel.created_at,
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_file_path(self, commit_id: int, file_path: str) -> list[ReviewComment]:
        """Get review comments for a specific file in a commit."""
        stmt = (
            select(ReviewCommentModel)
            .where(
                and_(
                    ReviewCommentModel.commit_id == commit_id,
                    ReviewCommentModel.file_path == file_path,
                )
            )
            .order_by(ReviewCommentModel.line_number, ReviewCommentModel.created_at)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def update(self, review_comment: ReviewComment) -> ReviewComment:
        """Update an existing review comment."""
        stmt = select(ReviewCommentModel).where(ReviewCommentModel.id == review_comment.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        # Update fields
        model.content = review_comment.content
        model.updated_at = review_comment.updated_at

        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def delete(self, comment_id: int) -> bool:
        """Delete a review comment."""
        stmt = delete(ReviewCommentModel).where(ReviewCommentModel.id == comment_id)
        result = await self.session.execute(stmt)

        return result.rowcount > 0

    async def get_line_comments(
        self, commit_id: int, file_path: str, line_number: int
    ) -> list[ReviewComment]:
        """Get review comments for a specific line in a file."""
        stmt = (
            select(ReviewCommentModel)
            .where(
                and_(
                    ReviewCommentModel.commit_id == commit_id,
                    ReviewCommentModel.file_path == file_path,
                    ReviewCommentModel.line_number == line_number,
                )
            )
            .order_by(ReviewCommentModel.created_at)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    def _model_to_entity(self, model: ReviewCommentModel) -> ReviewComment:
        """Convert SQLAlchemy model to domain entity."""
        return ReviewComment(
            id=model.id,
            commit_id=model.commit_id,
            reviewer_id=model.reviewer_id,
            line_number=model.line_number,
            file_path=model.file_path,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SqlAlchemyCommitReviewRepository(CommitReviewRepository):
    """SQLAlchemy implementation of CommitReviewRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, commit_review: CommitReview) -> CommitReview:
        """Create a new commit review."""
        model = CommitReviewModel(
            commit_id=commit_review.commit_id,
            reviewer_id=commit_review.reviewer_id,
            status=commit_review.status,
            reviewed_at=commit_review.reviewed_at,
            created_at=commit_review.created_at,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def get_by_id(self, review_id: int) -> CommitReview | None:
        """Get a commit review by ID."""
        stmt = select(CommitReviewModel).where(CommitReviewModel.id == review_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def get_by_commit_id(self, commit_id: int) -> list[CommitReview]:
        """Get all reviews for a commit."""
        stmt = (
            select(CommitReviewModel)
            .where(CommitReviewModel.commit_id == commit_id)
            .order_by(CommitReviewModel.created_at)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_reviewer_id(self, reviewer_id: int) -> list[CommitReview]:
        """Get all reviews by a specific reviewer."""
        stmt = (
            select(CommitReviewModel)
            .where(CommitReviewModel.reviewer_id == reviewer_id)
            .order_by(CommitReviewModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_commit_and_reviewer(
        self, commit_id: int, reviewer_id: int
    ) -> CommitReview | None:
        """Get a review for a commit by a specific reviewer."""
        stmt = select(CommitReviewModel).where(
            and_(
                CommitReviewModel.commit_id == commit_id,
                CommitReviewModel.reviewer_id == reviewer_id,
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def get_by_status(self, status: str) -> list[CommitReview]:
        """Get all reviews with a specific status."""
        stmt = (
            select(CommitReviewModel)
            .where(CommitReviewModel.status == status)
            .order_by(CommitReviewModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_pending_reviews(self, reviewer_id: int | None = None) -> list[CommitReview]:
        """Get all pending reviews, optionally filtered by reviewer."""
        stmt = select(CommitReviewModel).where(
            CommitReviewModel.status == CommitReview.ReviewStatus.PENDING
        )

        if reviewer_id:
            stmt = stmt.where(CommitReviewModel.reviewer_id == reviewer_id)

        stmt = stmt.order_by(CommitReviewModel.created_at)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_completed_reviews(
        self, reviewer_id: int | None = None, limit: int | None = None
    ) -> list[CommitReview]:
        """Get completed reviews, optionally filtered by reviewer with limit."""
        stmt = select(CommitReviewModel).where(
            CommitReviewModel.status.in_(
                [CommitReview.ReviewStatus.APPROVED, CommitReview.ReviewStatus.NEEDS_REVISION]
            )
        )

        if reviewer_id:
            stmt = stmt.where(CommitReviewModel.reviewer_id == reviewer_id)

        stmt = stmt.order_by(CommitReviewModel.reviewed_at.desc())

        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def update(self, commit_review: CommitReview) -> CommitReview:
        """Update an existing commit review."""
        stmt = select(CommitReviewModel).where(CommitReviewModel.id == commit_review.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        # Update fields
        model.status = commit_review.status
        model.reviewed_at = commit_review.reviewed_at

        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def delete(self, review_id: int) -> bool:
        """Delete a commit review."""
        stmt = delete(CommitReviewModel).where(CommitReviewModel.id == review_id)
        result = await self.session.execute(stmt)

        return result.rowcount > 0

    async def get_review_stats(self, reviewer_id: int | None = None) -> dict:
        """Get review statistics (count by status, average time, etc.)."""
        # Base query
        base_query = select(CommitReviewModel)
        if reviewer_id:
            base_query = base_query.where(CommitReviewModel.reviewer_id == reviewer_id)

        # Count by status
        status_counts = {}
        for status in CommitReview.ReviewStatus.all_values():
            stmt = base_query.where(CommitReviewModel.status == status)
            result = await self.session.execute(select(func.count()).select_from(stmt.subquery()))
            status_counts[status] = result.scalar()

        # Average review time for completed reviews
        completed_stmt = base_query.where(
            CommitReviewModel.status.in_(
                [CommitReview.ReviewStatus.APPROVED, CommitReview.ReviewStatus.NEEDS_REVISION]
            )
        ).where(CommitReviewModel.reviewed_at.is_not(None))

        avg_time_stmt = select(
            func.avg(
                func.extract("epoch", CommitReviewModel.reviewed_at - CommitReviewModel.created_at)
            )
        ).select_from(completed_stmt.subquery())

        result = await self.session.execute(avg_time_stmt)
        avg_review_time_seconds = result.scalar()

        return {
            "status_counts": status_counts,
            "total_reviews": sum(status_counts.values()),
            "avg_review_time_seconds": avg_review_time_seconds or 0,
            "avg_review_time_hours": (avg_review_time_seconds or 0) / 3600,
        }

    async def get_commits_needing_review(
        self, repository_id: int | None = None, limit: int | None = None
    ) -> list[int]:
        """Get commit IDs that need review (no pending/completed reviews)."""
        from haven.infrastructure.database.models import CommitModel

        # Subquery for commits that have reviews
        reviewed_commits_subquery = select(distinct(CommitReviewModel.commit_id))

        # Main query for commits without reviews
        stmt = select(CommitModel.id).where(CommitModel.id.not_in(reviewed_commits_subquery))

        if repository_id:
            stmt = stmt.where(CommitModel.repository_id == repository_id)

        stmt = stmt.order_by(CommitModel.committed_at.desc())

        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    def _model_to_entity(self, model: CommitReviewModel) -> CommitReview:
        """Convert SQLAlchemy model to domain entity."""
        return CommitReview(
            id=model.id,
            commit_id=model.commit_id,
            reviewer_id=model.reviewer_id,
            status=model.status,
            reviewed_at=model.reviewed_at,
            created_at=model.created_at,
        )
