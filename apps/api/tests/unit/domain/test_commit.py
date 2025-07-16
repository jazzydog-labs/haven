"""Tests for Commit domain entity."""

import pytest
from datetime import datetime, timezone

from haven.domain.entities.commit import Commit, CommitReview, DiffStats, ReviewStatus


class TestDiffStats:
    """Tests for DiffStats entity."""

    def test_create_diff_stats(self):
        """Test creating DiffStats."""
        stats = DiffStats(
            files_changed=5,
            insertions=100,
            deletions=50,
        )
        
        assert stats.files_changed == 5
        assert stats.insertions == 100
        assert stats.deletions == 50
        assert stats.total_changes == 150

    def test_diff_stats_defaults(self):
        """Test DiffStats with default values."""
        stats = DiffStats()
        
        assert stats.files_changed == 0
        assert stats.insertions == 0
        assert stats.deletions == 0
        assert stats.total_changes == 0


class TestCommit:
    """Tests for Commit entity."""

    def test_create_commit(self):
        """Test creating a valid commit."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats(files_changed=3, insertions=50, deletions=25)
        
        commit = Commit(
            repository_id=1,
            commit_hash="abc123def456",
            message="Add new feature",
            author_name="John Doe",
            author_email="john@example.com",
            committer_name="John Doe",
            committer_email="john@example.com",
            committed_at=now,
            diff_stats=diff_stats,
        )
        
        assert commit.repository_id == 1
        assert commit.commit_hash == "abc123def456"
        assert commit.message == "Add new feature"
        assert commit.author_name == "John Doe"
        assert commit.author_email == "john@example.com"
        assert commit.committer_name == "John Doe"
        assert commit.committer_email == "john@example.com"
        assert commit.committed_at == now
        assert commit.diff_stats == diff_stats
        assert commit.short_hash == "abc123d"
        assert commit.summary == "Add new feature"
        assert not commit.is_merge_commit

    def test_commit_validation_empty_hash(self):
        """Test commit validation with empty hash."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats()
        
        with pytest.raises(ValueError, match="Commit hash is required"):
            Commit(
                repository_id=1,
                commit_hash="",
                message="Add new feature",
                author_name="John Doe",
                author_email="john@example.com",
                committer_name="John Doe",
                committer_email="john@example.com",
                committed_at=now,
                diff_stats=diff_stats,
            )

    def test_commit_validation_short_hash(self):
        """Test commit validation with short hash."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats()
        
        with pytest.raises(ValueError, match="Commit hash must be at least 7 characters"):
            Commit(
                repository_id=1,
                commit_hash="abc123",
                message="Add new feature",
                author_name="John Doe",
                author_email="john@example.com",
                committer_name="John Doe",
                committer_email="john@example.com",
                committed_at=now,
                diff_stats=diff_stats,
            )

    def test_commit_validation_empty_message(self):
        """Test commit validation with empty message."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats()
        
        with pytest.raises(ValueError, match="Commit message is required"):
            Commit(
                repository_id=1,
                commit_hash="abc123def456",
                message="",
                author_name="John Doe",
                author_email="john@example.com",
                committer_name="John Doe",
                committer_email="john@example.com",
                committed_at=now,
                diff_stats=diff_stats,
            )

    def test_commit_validation_invalid_repository_id(self):
        """Test commit validation with invalid repository ID."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats()
        
        with pytest.raises(ValueError, match="Repository ID must be positive"):
            Commit(
                repository_id=0,
                commit_hash="abc123def456",
                message="Add new feature",
                author_name="John Doe",
                author_email="john@example.com",
                committer_name="John Doe",
                committer_email="john@example.com",
                committed_at=now,
                diff_stats=diff_stats,
            )

    def test_commit_merge_detection(self):
        """Test merge commit detection."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats()
        
        commit = Commit(
            repository_id=1,
            commit_hash="abc123def456",
            message="Merge branch 'feature' into main",
            author_name="John Doe",
            author_email="john@example.com",
            committer_name="John Doe",
            committer_email="john@example.com",
            committed_at=now,
            diff_stats=diff_stats,
        )
        
        assert commit.is_merge_commit

    def test_commit_multiline_message_summary(self):
        """Test summary extraction from multiline message."""
        now = datetime.now(timezone.utc)
        diff_stats = DiffStats()
        
        commit = Commit(
            repository_id=1,
            commit_hash="abc123def456",
            message="Add new feature\n\nThis is a detailed description\nof the feature implementation.",
            author_name="John Doe",
            author_email="john@example.com",
            committer_name="John Doe",
            committer_email="john@example.com",
            committed_at=now,
            diff_stats=diff_stats,
        )
        
        assert commit.summary == "Add new feature"


class TestCommitReview:
    """Tests for CommitReview entity."""

    def test_create_commit_review(self):
        """Test creating a valid commit review."""
        now = datetime.now(timezone.utc)
        
        review = CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=ReviewStatus.PENDING_REVIEW,
            notes="Looks good, but needs tests",
            reviewed_at=now,
        )
        
        assert review.commit_id == 1
        assert review.reviewer_id == 2
        assert review.status == ReviewStatus.PENDING_REVIEW
        assert review.notes == "Looks good, but needs tests"
        assert review.reviewed_at == now
        assert not review.is_approved
        assert review.needs_action

    def test_commit_review_validation_invalid_commit_id(self):
        """Test commit review validation with invalid commit ID."""
        with pytest.raises(ValueError, match="Commit ID must be positive"):
            CommitReview(
                commit_id=0,
                reviewer_id=2,
                status=ReviewStatus.PENDING_REVIEW,
            )

    def test_commit_review_validation_invalid_reviewer_id(self):
        """Test commit review validation with invalid reviewer ID."""
        with pytest.raises(ValueError, match="Reviewer ID must be positive"):
            CommitReview(
                commit_id=1,
                reviewer_id=0,
                status=ReviewStatus.PENDING_REVIEW,
            )

    def test_commit_review_validation_invalid_status(self):
        """Test commit review validation with invalid status."""
        with pytest.raises(ValueError, match="Status must be a valid ReviewStatus"):
            CommitReview(
                commit_id=1,
                reviewer_id=2,
                status="invalid_status",
            )

    def test_commit_review_approved_status(self):
        """Test approved review status."""
        review = CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=ReviewStatus.APPROVED,
        )
        
        assert review.is_approved
        assert not review.needs_action

    def test_commit_review_needs_revision_status(self):
        """Test needs revision review status."""
        review = CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=ReviewStatus.NEEDS_REVISION,
        )
        
        assert not review.is_approved
        assert review.needs_action

    def test_commit_review_draft_status(self):
        """Test draft review status."""
        review = CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=ReviewStatus.DRAFT,
        )
        
        assert not review.is_approved
        assert not review.needs_action