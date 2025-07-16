"""Tests for CommitService."""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from haven.application.services.commit_service import CommitService
from haven.domain.entities.commit import Commit, CommitReview, DiffStats, ReviewStatus


class TestCommitService:
    """Tests for CommitService."""

    @pytest.fixture
    def mock_commit_repository(self):
        """Create mock commit repository."""
        return AsyncMock()

    @pytest.fixture
    def mock_commit_review_repository(self):
        """Create mock commit review repository."""
        return AsyncMock()

    @pytest.fixture
    def commit_service(self, mock_commit_repository, mock_commit_review_repository):
        """Create commit service for testing."""
        return CommitService(mock_commit_repository, mock_commit_review_repository)

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
            committed_at=datetime.now(timezone.utc),
            diff_stats=DiffStats(files_changed=3, insertions=50, deletions=25),
        )

    @pytest.fixture
    def sample_commit_review(self):
        """Create sample commit review for testing."""
        return CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=ReviewStatus.PENDING_REVIEW,
            notes="Looks good, but needs tests",
        )

    @pytest.mark.asyncio
    async def test_create_commit(self, commit_service, mock_commit_repository, sample_commit):
        """Test creating a commit."""
        mock_commit_repository.get_by_hash.return_value = None
        mock_commit_repository.create.return_value = sample_commit

        result = await commit_service.create_commit(sample_commit)

        assert result == sample_commit
        mock_commit_repository.get_by_hash.assert_called_once_with(
            sample_commit.repository_id, sample_commit.commit_hash
        )
        mock_commit_repository.create.assert_called_once_with(sample_commit)

    @pytest.mark.asyncio
    async def test_create_commit_already_exists(self, commit_service, mock_commit_repository, sample_commit):
        """Test creating a commit that already exists."""
        mock_commit_repository.get_by_hash.return_value = sample_commit

        with pytest.raises(ValueError, match="Commit abc123def456 already exists"):
            await commit_service.create_commit(sample_commit)

        mock_commit_repository.get_by_hash.assert_called_once_with(
            sample_commit.repository_id, sample_commit.commit_hash
        )
        mock_commit_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_commit_by_id(self, commit_service, mock_commit_repository, sample_commit):
        """Test getting a commit by ID."""
        mock_commit_repository.get_by_id.return_value = sample_commit

        result = await commit_service.get_commit_by_id(1)

        assert result == sample_commit
        mock_commit_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_commit_by_hash(self, commit_service, mock_commit_repository, sample_commit):
        """Test getting a commit by hash."""
        mock_commit_repository.get_by_hash.return_value = sample_commit

        result = await commit_service.get_commit_by_hash(1, "abc123def456")

        assert result == sample_commit
        mock_commit_repository.get_by_hash.assert_called_once_with(1, "abc123def456")

    @pytest.mark.asyncio
    async def test_get_commits_by_repository(self, commit_service, mock_commit_repository, sample_commit):
        """Test getting commits by repository."""
        mock_commit_repository.get_by_repository.return_value = [sample_commit]

        result = await commit_service.get_commits_by_repository(1)

        assert result == [sample_commit]
        mock_commit_repository.get_by_repository.assert_called_once_with(1, 100, 0)

    @pytest.mark.asyncio
    async def test_update_commit(self, commit_service, mock_commit_repository, sample_commit):
        """Test updating a commit."""
        sample_commit.id = 1
        mock_commit_repository.get_by_id.return_value = sample_commit
        mock_commit_repository.update.return_value = sample_commit

        result = await commit_service.update_commit(sample_commit)

        assert result == sample_commit
        mock_commit_repository.get_by_id.assert_called_once_with(1)
        mock_commit_repository.update.assert_called_once_with(sample_commit)

    @pytest.mark.asyncio
    async def test_update_commit_no_id(self, commit_service, sample_commit):
        """Test updating a commit without ID."""
        with pytest.raises(ValueError, match="Commit ID is required for update"):
            await commit_service.update_commit(sample_commit)

    @pytest.mark.asyncio
    async def test_update_commit_not_found(self, commit_service, mock_commit_repository, sample_commit):
        """Test updating a commit that doesn't exist."""
        sample_commit.id = 1
        mock_commit_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Commit 1 not found"):
            await commit_service.update_commit(sample_commit)

    @pytest.mark.asyncio
    async def test_delete_commit(self, commit_service, mock_commit_repository):
        """Test deleting a commit."""
        mock_commit_repository.delete.return_value = True

        result = await commit_service.delete_commit(1)

        assert result is True
        mock_commit_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_sync_commits_from_git(self, commit_service, mock_commit_repository, sample_commit):
        """Test syncing commits from Git."""
        git_commits = [
            {
                "hash": "abc123def456",
                "message": "Add new feature",
                "author_name": "John Doe",
                "author_email": "john@example.com",
                "committer_name": "John Doe",
                "committer_email": "john@example.com",
                "committed_at": datetime.now(timezone.utc),
                "diff_stats": DiffStats(files_changed=3, insertions=50, deletions=25),
            }
        ]

        mock_commit_repository.get_by_hash.return_value = None
        mock_commit_repository.create.return_value = sample_commit

        result = await commit_service.sync_commits_from_git(1, git_commits)

        assert len(result) == 1
        assert result[0] == sample_commit
        mock_commit_repository.get_by_hash.assert_called_once_with(1, "abc123def456")
        mock_commit_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_sync_commits_from_git_existing(self, commit_service, mock_commit_repository, sample_commit):
        """Test syncing commits from Git with existing commit."""
        git_commits = [
            {
                "hash": "abc123def456",
                "message": "Add new feature",
                "author_name": "John Doe",
                "author_email": "john@example.com",
                "committer_name": "John Doe",
                "committer_email": "john@example.com",
                "committed_at": datetime.now(timezone.utc),
                "diff_stats": DiffStats(files_changed=3, insertions=50, deletions=25),
            }
        ]

        mock_commit_repository.get_by_hash.return_value = sample_commit

        result = await commit_service.sync_commits_from_git(1, git_commits)

        assert len(result) == 1
        assert result[0] == sample_commit
        mock_commit_repository.get_by_hash.assert_called_once_with(1, "abc123def456")
        mock_commit_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_commit_review(self, commit_service, mock_commit_repository, mock_commit_review_repository, sample_commit, sample_commit_review):
        """Test creating a commit review."""
        mock_commit_repository.get_by_id.return_value = sample_commit
        mock_commit_review_repository.create.return_value = sample_commit_review

        result = await commit_service.create_commit_review(sample_commit_review)

        assert result == sample_commit_review
        mock_commit_repository.get_by_id.assert_called_once_with(sample_commit_review.commit_id)
        mock_commit_review_repository.create.assert_called_once_with(sample_commit_review)

    @pytest.mark.asyncio
    async def test_create_commit_review_commit_not_found(self, commit_service, mock_commit_repository, mock_commit_review_repository, sample_commit_review):
        """Test creating a commit review for non-existent commit."""
        mock_commit_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Commit 1 not found"):
            await commit_service.create_commit_review(sample_commit_review)

        mock_commit_repository.get_by_id.assert_called_once_with(sample_commit_review.commit_id)
        mock_commit_review_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_commit_with_reviews(self, commit_service, mock_commit_repository, mock_commit_review_repository, sample_commit, sample_commit_review):
        """Test getting a commit with reviews."""
        mock_commit_repository.get_by_id.return_value = sample_commit
        mock_commit_review_repository.get_by_commit.return_value = [sample_commit_review]

        result = await commit_service.get_commit_with_reviews(1)

        assert result["commit"] == sample_commit
        assert result["reviews"] == [sample_commit_review]
        assert result["review_status"] == "pending_review"

    @pytest.mark.asyncio
    async def test_get_commit_with_reviews_not_found(self, commit_service, mock_commit_repository):
        """Test getting a commit with reviews when commit doesn't exist."""
        mock_commit_repository.get_by_id.return_value = None

        result = await commit_service.get_commit_with_reviews(1)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_overall_review_status_no_reviews(self, commit_service):
        """Test overall review status with no reviews."""
        result = commit_service._get_overall_review_status([])
        assert result == "no_reviews"

    @pytest.mark.asyncio
    async def test_get_overall_review_status_needs_revision(self, commit_service):
        """Test overall review status with needs revision."""
        reviews = [
            CommitReview(1, 2, ReviewStatus.APPROVED),
            CommitReview(1, 3, ReviewStatus.NEEDS_REVISION),
        ]
        result = commit_service._get_overall_review_status(reviews)
        assert result == "needs_revision"

    @pytest.mark.asyncio
    async def test_get_overall_review_status_approved(self, commit_service):
        """Test overall review status with all approved."""
        reviews = [
            CommitReview(1, 2, ReviewStatus.APPROVED),
            CommitReview(1, 3, ReviewStatus.APPROVED),
        ]
        result = commit_service._get_overall_review_status(reviews)
        assert result == "approved"

    @pytest.mark.asyncio
    async def test_get_overall_review_status_pending(self, commit_service):
        """Test overall review status with pending reviews."""
        reviews = [
            CommitReview(1, 2, ReviewStatus.APPROVED),
            CommitReview(1, 3, ReviewStatus.PENDING_REVIEW),
        ]
        result = commit_service._get_overall_review_status(reviews)
        assert result == "pending_review"