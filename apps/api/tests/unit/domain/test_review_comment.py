"""Tests for review comment domain entities."""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from haven.domain.entities.review_comment import ReviewComment, CommitReview


class TestReviewComment:
    """Test ReviewComment domain entity."""
    
    def test_create_review_comment_minimal(self):
        """Test creating a review comment with minimal required fields."""
        comment = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="This looks good!"
        )
        
        assert comment.commit_id == 1
        assert comment.reviewer_id == 1
        assert comment.content == "This looks good!"
        assert comment.line_number is None
        assert comment.file_path is None
        assert isinstance(comment.created_at, datetime)
        assert comment.updated_at is None
    
    def test_create_line_comment(self):
        """Test creating a line-specific comment."""
        comment = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            line_number=42,
            file_path="src/main.py",
            content="Consider adding error handling here."
        )
        
        assert comment.line_number == 42
        assert comment.file_path == "src/main.py"
        assert comment.is_line_comment is True
        assert comment.is_file_comment is False
        assert comment.is_general_comment is False
    
    def test_create_file_comment(self):
        """Test creating a file-specific comment."""
        comment = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            file_path="src/main.py",
            content="This file needs better documentation."
        )
        
        assert comment.file_path == "src/main.py"
        assert comment.line_number is None
        assert comment.is_line_comment is False
        assert comment.is_file_comment is True
        assert comment.is_general_comment is False
    
    def test_create_general_comment(self):
        """Test creating a general commit comment."""
        comment = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="Overall this commit looks good."
        )
        
        assert comment.file_path is None
        assert comment.line_number is None
        assert comment.is_line_comment is False
        assert comment.is_file_comment is False
        assert comment.is_general_comment is True
    
    def test_validate_line_number_positive(self):
        """Test that line number must be positive."""
        with pytest.raises(ValidationError) as exc_info:
            ReviewComment(
                commit_id=1,
                reviewer_id=1,
                line_number=0,
                content="Test comment"
            )
        assert "Line number must be positive" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            ReviewComment(
                commit_id=1,
                reviewer_id=1,
                line_number=-5,
                content="Test comment"
            )
        assert "Line number must be positive" in str(exc_info.value)
    
    def test_validate_file_path_format(self):
        """Test file path validation."""
        # Should reject absolute paths
        with pytest.raises(ValidationError) as exc_info:
            ReviewComment(
                commit_id=1,
                reviewer_id=1,
                file_path="/absolute/path.py",
                content="Test comment"
            )
        assert "should be relative" in str(exc_info.value)
        
        # Should reject paths with ..
        with pytest.raises(ValidationError) as exc_info:
            ReviewComment(
                commit_id=1,
                reviewer_id=1,
                file_path="../parent/file.py",
                content="Test comment"
            )
        assert "cannot contain .. sequences" in str(exc_info.value)
    
    def test_validate_content_not_empty(self):
        """Test that content cannot be empty or whitespace."""
        with pytest.raises(ValidationError) as exc_info:
            ReviewComment(
                commit_id=1,
                reviewer_id=1,
                content=""
            )
        assert "String should have at least 1 character" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            ReviewComment(
                commit_id=1,
                reviewer_id=1,
                content="   \n\t  "
            )
        assert "Comment content cannot be empty" in str(exc_info.value)
    
    def test_content_whitespace_trimmed(self):
        """Test that content whitespace is trimmed."""
        comment = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="  Good work!  \n"
        )
        assert comment.content == "Good work!"
    
    def test_update_content(self):
        """Test updating comment content."""
        original = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="Original content"
        )
        
        updated = original.update_content("Updated content")
        
        assert updated.content == "Updated content"
        assert updated.updated_at is not None
        assert updated.created_at == original.created_at
        assert updated.id == original.id
        assert updated.commit_id == original.commit_id


class TestCommitReview:
    """Test CommitReview domain entity."""
    
    def test_create_commit_review(self):
        """Test creating a commit review."""
        review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        assert review.commit_id == 1
        assert review.reviewer_id == 1
        assert review.status == "pending"
        assert isinstance(review.created_at, datetime)
        assert review.reviewed_at is None
    
    def test_validate_status(self):
        """Test review status validation."""
        # Valid statuses should work
        for status in CommitReview.ReviewStatus.all_values():
            review = CommitReview(
                commit_id=1,
                reviewer_id=1,
                status=status
            )
            assert review.status == status
        
        # Invalid status should fail
        with pytest.raises(ValidationError) as exc_info:
            CommitReview(
                commit_id=1,
                reviewer_id=1,
                status="invalid_status"
            )
        assert "Status must be one of" in str(exc_info.value)
    
    def test_review_status_properties(self):
        """Test review status property methods."""
        # Test draft
        draft_review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.DRAFT
        )
        assert draft_review.is_draft is True
        assert draft_review.is_pending is False
        assert draft_review.is_completed is False
        
        # Test pending
        pending_review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        assert pending_review.is_draft is False
        assert pending_review.is_pending is True
        assert pending_review.is_completed is False
        
        # Test approved
        approved_review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.APPROVED
        )
        assert approved_review.is_draft is False
        assert approved_review.is_pending is False
        assert approved_review.is_completed is True
        
        # Test needs revision
        needs_revision_review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.NEEDS_REVISION
        )
        assert needs_revision_review.is_draft is False
        assert needs_revision_review.is_pending is False
        assert needs_revision_review.is_completed is True
    
    def test_complete_review_approved(self):
        """Test completing a review with approved status."""
        original = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        completed = original.complete_review(CommitReview.ReviewStatus.APPROVED)
        
        assert completed.status == CommitReview.ReviewStatus.APPROVED
        assert completed.reviewed_at is not None
        assert completed.is_completed is True
    
    def test_complete_review_needs_revision(self):
        """Test completing a review with needs revision status."""
        original = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        completed = original.complete_review(CommitReview.ReviewStatus.NEEDS_REVISION)
        
        assert completed.status == CommitReview.ReviewStatus.NEEDS_REVISION
        assert completed.reviewed_at is not None
        assert completed.is_completed is True
    
    def test_complete_review_invalid_status(self):
        """Test that complete_review rejects invalid completion statuses."""
        review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        with pytest.raises(ValueError) as exc_info:
            review.complete_review(CommitReview.ReviewStatus.DRAFT)
        assert "must be approved or needs_revision" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            review.complete_review(CommitReview.ReviewStatus.PENDING)
        assert "must be approved or needs_revision" in str(exc_info.value)
    
    def test_update_status(self):
        """Test updating review status."""
        original = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.DRAFT
        )
        
        # Update to pending (non-completion status)
        pending = original.update_status(CommitReview.ReviewStatus.PENDING)
        assert pending.status == CommitReview.ReviewStatus.PENDING
        assert pending.reviewed_at is None  # Should not set reviewed_at
        
        # Update to approved (completion status)
        approved = pending.update_status(CommitReview.ReviewStatus.APPROVED)
        assert approved.status == CommitReview.ReviewStatus.APPROVED
        assert approved.reviewed_at is not None  # Should set reviewed_at
    
    def test_all_status_values(self):
        """Test that all status values are returned correctly."""
        expected = ['draft', 'pending', 'approved', 'needs_revision']
        assert CommitReview.ReviewStatus.all_values() == expected