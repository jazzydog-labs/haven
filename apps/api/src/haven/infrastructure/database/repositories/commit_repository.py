"""SQLAlchemy implementation of CommitRepository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.commit import Commit, CommitReview, DiffStats, ReviewStatus
from haven.domain.repositories.commit_repository import CommitRepository, CommitReviewRepository
from haven.infrastructure.database.models import CommitModel, CommitReviewModel


class SQLAlchemyCommitRepository(CommitRepository):
    """SQLAlchemy implementation of CommitRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, commit: Commit) -> Commit:
        """Create a new commit."""
        model = CommitModel(
            repository_id=commit.repository_id,
            commit_hash=commit.commit_hash,
            message=commit.message,
            author_name=commit.author_name,
            author_email=commit.author_email,
            committer_name=commit.committer_name,
            committer_email=commit.committer_email,
            committed_at=commit.committed_at,
            files_changed=commit.diff_stats.files_changed,
            insertions=commit.diff_stats.insertions,
            deletions=commit.diff_stats.deletions,
            diff_html_path=commit.diff_html_path,
            diff_generated_at=commit.diff_generated_at,
        )

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def get_by_id(self, commit_id: int) -> Commit | None:
        """Get a commit by ID."""
        stmt = select(CommitModel).where(CommitModel.id == commit_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def get_by_hash(self, repository_id: int, commit_hash: str) -> Commit | None:
        """Get a commit by repository and hash."""
        stmt = select(CommitModel).where(
            CommitModel.repository_id == repository_id, CommitModel.commit_hash == commit_hash
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._model_to_entity(model) if model else None

    async def get_by_repository(
        self, repository_id: int, limit: int = 100, offset: int = 0
    ) -> list[Commit]:
        """Get commits for a repository."""
        stmt = (
            select(CommitModel)
            .where(CommitModel.repository_id == repository_id)
            .order_by(CommitModel.committed_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def update(self, commit: Commit) -> Commit:
        """Update an existing commit."""
        stmt = select(CommitModel).where(CommitModel.id == commit.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        # Update fields
        model.message = commit.message
        model.author_name = commit.author_name
        model.author_email = commit.author_email
        model.committer_name = commit.committer_name
        model.committer_email = commit.committer_email
        model.committed_at = commit.committed_at
        model.files_changed = commit.diff_stats.files_changed
        model.insertions = commit.diff_stats.insertions
        model.deletions = commit.diff_stats.deletions
        model.diff_html_path = commit.diff_html_path
        model.diff_generated_at = commit.diff_generated_at

        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def delete(self, commit_id: int) -> bool:
        """Delete a commit."""
        stmt = select(CommitModel).where(CommitModel.id == commit_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False

    async def exists_by_hash(self, repository_id: int, commit_hash: str) -> bool:
        """Check if a commit exists by hash."""
        stmt = select(CommitModel.id).where(
            CommitModel.repository_id == repository_id, CommitModel.commit_hash == commit_hash
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _model_to_entity(self, model: CommitModel) -> Commit:
        """Convert CommitModel to Commit entity."""
        return Commit(
            id=model.id,
            repository_id=model.repository_id,
            commit_hash=model.commit_hash,
            message=model.message,
            author_name=model.author_name,
            author_email=model.author_email,
            committer_name=model.committer_name,
            committer_email=model.committer_email,
            committed_at=model.committed_at,
            diff_stats=DiffStats(
                files_changed=model.files_changed,
                insertions=model.insertions,
                deletions=model.deletions,
            ),
            diff_html_path=model.diff_html_path,
            diff_generated_at=model.diff_generated_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyCommitReviewRepository(CommitReviewRepository):
    """SQLAlchemy implementation of CommitReviewRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, review: CommitReview) -> CommitReview:
        """Create a new commit review."""
        model = CommitReviewModel(
            commit_id=review.commit_id,
            reviewer_id=review.reviewer_id,
            status=review.status.value,
            notes=review.notes,
            reviewed_at=review.reviewed_at,
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

    async def get_by_commit(self, commit_id: int) -> list[CommitReview]:
        """Get all reviews for a commit."""
        stmt = (
            select(CommitReviewModel)
            .where(CommitReviewModel.commit_id == commit_id)
            .order_by(CommitReviewModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def get_by_reviewer(
        self, reviewer_id: int, limit: int = 100, offset: int = 0
    ) -> list[CommitReview]:
        """Get reviews by reviewer."""
        stmt = (
            select(CommitReviewModel)
            .where(CommitReviewModel.reviewer_id == reviewer_id)
            .order_by(CommitReviewModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]

    async def update(self, review: CommitReview) -> CommitReview:
        """Update an existing commit review."""
        stmt = select(CommitReviewModel).where(CommitReviewModel.id == review.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        # Update fields
        model.status = review.status.value
        model.notes = review.notes
        model.reviewed_at = review.reviewed_at

        await self.session.flush()
        await self.session.refresh(model)

        return self._model_to_entity(model)

    async def delete(self, review_id: int) -> bool:
        """Delete a commit review."""
        stmt = select(CommitReviewModel).where(CommitReviewModel.id == review_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False

    def _model_to_entity(self, model: CommitReviewModel) -> CommitReview:
        """Convert CommitReviewModel to CommitReview entity."""
        return CommitReview(
            id=model.id,
            commit_id=model.commit_id,
            reviewer_id=model.reviewer_id,
            status=ReviewStatus(model.status),
            notes=model.notes,
            reviewed_at=model.reviewed_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
