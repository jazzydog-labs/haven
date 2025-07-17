"""Tests for SQLAlchemy Commit repository implementation."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.commit import Commit, CommitReview, DiffStats, ReviewStatus
from haven.infrastructure.database.repositories.commit_repository import (
    SQLAlchemyCommitRepository,
    SQLAlchemyCommitReviewRepository,
)


class TestSQLAlchemyCommitRepository:
    """Tests for SQLAlchemy Commit repository."""

    @pytest.fixture
    def commit_repository(self, test_session: AsyncSession):
        """Create commit repository for testing."""
        return SQLAlchemyCommitRepository(test_session)

    @pytest.fixture
    def sample_commit(self):
        """Create sample commit for testing."""
        return Commit(
            repository_id=1,
            commit_hash="abc123def456",
            message="Add new feature",
            author_name="John Doe",
            author_email="john@example.com",
            committer_name="John Doe",
            committer_email="john@example.com",
            committed_at=datetime.now(UTC),
            diff_stats=DiffStats(files_changed=3, insertions=50, deletions=25),
        )

    @pytest.mark.asyncio
    async def test_create_commit(self, commit_repository, sample_commit):
        """Test creating a commit."""
        created_commit = await commit_repository.create(sample_commit)

        assert created_commit.id is not None
        assert created_commit.repository_id == sample_commit.repository_id
        assert created_commit.commit_hash == sample_commit.commit_hash
        assert created_commit.message == sample_commit.message
        assert created_commit.author_name == sample_commit.author_name
        assert created_commit.diff_stats.files_changed == 3
        assert created_commit.diff_stats.insertions == 50
        assert created_commit.diff_stats.deletions == 25
        assert created_commit.created_at is not None
        assert created_commit.updated_at is not None

    @pytest.mark.asyncio
    async def test_get_commit_by_id(self, commit_repository, sample_commit):
        """Test getting a commit by ID."""
        created_commit = await commit_repository.create(sample_commit)

        retrieved_commit = await commit_repository.get_by_id(created_commit.id)

        assert retrieved_commit is not None
        assert retrieved_commit.id == created_commit.id
        assert retrieved_commit.commit_hash == sample_commit.commit_hash
        assert retrieved_commit.message == sample_commit.message

    @pytest.mark.asyncio
    async def test_get_commit_by_id_not_found(self, commit_repository):
        """Test getting a commit by ID when it doesn't exist."""
        retrieved_commit = await commit_repository.get_by_id(999)

        assert retrieved_commit is None

    @pytest.mark.asyncio
    async def test_get_commit_by_hash(self, commit_repository, sample_commit):
        """Test getting a commit by repository and hash."""
        created_commit = await commit_repository.create(sample_commit)

        retrieved_commit = await commit_repository.get_by_hash(
            sample_commit.repository_id, sample_commit.commit_hash
        )

        assert retrieved_commit is not None
        assert retrieved_commit.id == created_commit.id
        assert retrieved_commit.commit_hash == sample_commit.commit_hash

    @pytest.mark.asyncio
    async def test_get_commit_by_hash_not_found(self, commit_repository):
        """Test getting a commit by hash when it doesn't exist."""
        retrieved_commit = await commit_repository.get_by_hash(1, "nonexistent")

        assert retrieved_commit is None

    @pytest.mark.asyncio
    async def test_get_commits_by_repository(self, commit_repository, sample_commit):
        """Test getting commits for a repository."""
        # Create multiple commits
        commit1 = await commit_repository.create(sample_commit)

        commit2 = Commit(
            repository_id=1,
            commit_hash="def456abc789",
            message="Fix bug",
            author_name="Jane Doe",
            author_email="jane@example.com",
            committer_name="Jane Doe",
            committer_email="jane@example.com",
            committed_at=datetime.now(UTC),
            diff_stats=DiffStats(files_changed=1, insertions=10, deletions=5),
        )
        commit2 = await commit_repository.create(commit2)

        commits = await commit_repository.get_by_repository(1)

        assert len(commits) == 2
        # Should be ordered by committed_at desc
        assert commits[0].id in [commit1.id, commit2.id]
        assert commits[1].id in [commit1.id, commit2.id]

    @pytest.mark.asyncio
    async def test_get_commits_by_repository_with_pagination(
        self, commit_repository, sample_commit
    ):
        """Test getting commits with pagination."""
        # Create multiple commits
        for i in range(5):
            commit = Commit(
                repository_id=1,
                commit_hash=f"hash{i:03d}",
                message=f"Commit {i}",
                author_name="John Doe",
                author_email="john@example.com",
                committer_name="John Doe",
                committer_email="john@example.com",
                committed_at=datetime.now(UTC),
                diff_stats=DiffStats(files_changed=1, insertions=1, deletions=1),
            )
            await commit_repository.create(commit)

        # Test pagination
        commits = await commit_repository.get_by_repository(1, limit=2, offset=1)

        assert len(commits) == 2

    @pytest.mark.asyncio
    async def test_update_commit(self, commit_repository, sample_commit):
        """Test updating a commit."""
        created_commit = await commit_repository.create(sample_commit)

        # Update the commit
        created_commit.message = "Updated message"
        created_commit.diff_stats.insertions = 100

        updated_commit = await commit_repository.update(created_commit)

        assert updated_commit.message == "Updated message"
        assert updated_commit.diff_stats.insertions == 100

    @pytest.mark.asyncio
    async def test_delete_commit(self, commit_repository, sample_commit):
        """Test deleting a commit."""
        created_commit = await commit_repository.create(sample_commit)

        deleted = await commit_repository.delete(created_commit.id)

        assert deleted is True

        retrieved_commit = await commit_repository.get_by_id(created_commit.id)
        assert retrieved_commit is None

    @pytest.mark.asyncio
    async def test_delete_commit_not_found(self, commit_repository):
        """Test deleting a commit that doesn't exist."""
        deleted = await commit_repository.delete(999)

        assert deleted is False

    @pytest.mark.asyncio
    async def test_exists_by_hash(self, commit_repository, sample_commit):
        """Test checking if a commit exists by hash."""
        await commit_repository.create(sample_commit)

        exists = await commit_repository.exists_by_hash(
            sample_commit.repository_id, sample_commit.commit_hash
        )

        assert exists is True

    @pytest.mark.asyncio
    async def test_exists_by_hash_not_found(self, commit_repository):
        """Test checking if a commit exists by hash when it doesn't."""
        exists = await commit_repository.exists_by_hash(1, "nonexistent")

        assert exists is False


class TestSQLAlchemyCommitReviewRepository:
    """Tests for SQLAlchemy CommitReview repository."""

    @pytest.fixture
    def commit_review_repository(self, test_session: AsyncSession):
        """Create commit review repository for testing."""
        return SQLAlchemyCommitReviewRepository(test_session)

    @pytest.fixture
    def sample_commit_review(self):
        """Create sample commit review for testing."""
        return CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=ReviewStatus.PENDING_REVIEW,
            notes="Looks good, but needs tests",
            reviewed_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_create_commit_review(self, commit_review_repository, sample_commit_review):
        """Test creating a commit review."""
        created_review = await commit_review_repository.create(sample_commit_review)

        assert created_review.id is not None
        assert created_review.commit_id == sample_commit_review.commit_id
        assert created_review.reviewer_id == sample_commit_review.reviewer_id
        assert created_review.status == sample_commit_review.status
        assert created_review.notes == sample_commit_review.notes
        assert created_review.created_at is not None
        assert created_review.updated_at is not None

    @pytest.mark.asyncio
    async def test_get_commit_review_by_id(self, commit_review_repository, sample_commit_review):
        """Test getting a commit review by ID."""
        created_review = await commit_review_repository.create(sample_commit_review)

        retrieved_review = await commit_review_repository.get_by_id(created_review.id)

        assert retrieved_review is not None
        assert retrieved_review.id == created_review.id
        assert retrieved_review.status == sample_commit_review.status

    @pytest.mark.asyncio
    async def test_get_reviews_by_commit(self, commit_review_repository, sample_commit_review):
        """Test getting reviews for a commit."""
        # Create multiple reviews for the same commit
        review1 = await commit_review_repository.create(sample_commit_review)

        review2 = CommitReview(
            commit_id=1,
            reviewer_id=3,
            status=ReviewStatus.APPROVED,
        )
        review2 = await commit_review_repository.create(review2)

        reviews = await commit_review_repository.get_by_commit(1)

        assert len(reviews) == 2
        assert reviews[0].id in [review1.id, review2.id]
        assert reviews[1].id in [review1.id, review2.id]

    @pytest.mark.asyncio
    async def test_get_reviews_by_reviewer(self, commit_review_repository, sample_commit_review):
        """Test getting reviews by reviewer."""
        # Create multiple reviews by the same reviewer
        review1 = await commit_review_repository.create(sample_commit_review)

        review2 = CommitReview(
            commit_id=2,
            reviewer_id=2,
            status=ReviewStatus.APPROVED,
        )
        review2 = await commit_review_repository.create(review2)

        reviews = await commit_review_repository.get_by_reviewer(2)

        assert len(reviews) == 2
        assert reviews[0].id in [review1.id, review2.id]
        assert reviews[1].id in [review1.id, review2.id]

    @pytest.mark.asyncio
    async def test_update_commit_review(self, commit_review_repository, sample_commit_review):
        """Test updating a commit review."""
        created_review = await commit_review_repository.create(sample_commit_review)

        # Update the review
        created_review.status = ReviewStatus.APPROVED
        created_review.notes = "Updated notes"

        updated_review = await commit_review_repository.update(created_review)

        assert updated_review.status == ReviewStatus.APPROVED
        assert updated_review.notes == "Updated notes"

    @pytest.mark.asyncio
    async def test_delete_commit_review(self, commit_review_repository, sample_commit_review):
        """Test deleting a commit review."""
        created_review = await commit_review_repository.create(sample_commit_review)

        deleted = await commit_review_repository.delete(created_review.id)

        assert deleted is True

        retrieved_review = await commit_review_repository.get_by_id(created_review.id)
        assert retrieved_review is None
