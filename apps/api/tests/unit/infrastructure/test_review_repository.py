"""Tests for review repository implementations."""

import pytest
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.review_comment import ReviewComment, CommitReview
from haven.infrastructure.database.repositories.review_repository import (
    SqlAlchemyReviewCommentRepository,
    SqlAlchemyCommitReviewRepository
)


class TestSqlAlchemyReviewCommentRepository:
    """Test SqlAlchemyReviewCommentRepository."""
    
    @pytest.fixture
    async def repository(self, db_session: AsyncSession):
        """Create repository instance."""
        return SqlAlchemyReviewCommentRepository(db_session)
    
    @pytest.fixture
    async def sample_comment(self):
        """Create a sample review comment."""
        return ReviewComment(
            commit_id=1,
            reviewer_id=1,
            line_number=42,
            file_path="src/main.py",
            content="Consider adding error handling here."
        )
    
    async def test_create_review_comment(self, repository, sample_comment):
        """Test creating a review comment."""
        created = await repository.create(sample_comment)
        
        assert created.id is not None
        assert created.commit_id == sample_comment.commit_id
        assert created.reviewer_id == sample_comment.reviewer_id
        assert created.content == sample_comment.content
        assert isinstance(created.created_at, datetime)
    
    async def test_get_by_id(self, repository, sample_comment):
        """Test retrieving a review comment by ID."""
        created = await repository.create(sample_comment)
        
        retrieved = await repository.get_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.content == created.content
    
    async def test_get_by_id_not_found(self, repository):
        """Test retrieving a non-existent review comment."""
        result = await repository.get_by_id(99999)
        assert result is None
    
    async def test_get_by_commit_id(self, repository):
        """Test retrieving review comments by commit ID."""
        comment1 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="First comment"
        )
        comment2 = ReviewComment(
            commit_id=1,
            reviewer_id=2,
            content="Second comment"
        )
        comment3 = ReviewComment(
            commit_id=2,
            reviewer_id=1,
            content="Different commit"
        )
        
        await repository.create(comment1)
        await repository.create(comment2)
        await repository.create(comment3)
        
        comments = await repository.get_by_commit_id(1)
        
        assert len(comments) == 2
        assert all(c.commit_id == 1 for c in comments)
    
    async def test_get_by_reviewer_id(self, repository):
        """Test retrieving review comments by reviewer ID."""
        comment1 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="First comment"
        )
        comment2 = ReviewComment(
            commit_id=2,
            reviewer_id=1,
            content="Second comment"
        )
        comment3 = ReviewComment(
            commit_id=1,
            reviewer_id=2,
            content="Different reviewer"
        )
        
        await repository.create(comment1)
        await repository.create(comment2)
        await repository.create(comment3)
        
        comments = await repository.get_by_reviewer_id(1)
        
        assert len(comments) == 2
        assert all(c.reviewer_id == 1 for c in comments)
    
    async def test_get_by_commit_and_reviewer(self, repository):
        """Test retrieving review comments by commit and reviewer."""
        comment1 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            content="Target comment"
        )
        comment2 = ReviewComment(
            commit_id=1,
            reviewer_id=2,
            content="Different reviewer"
        )
        comment3 = ReviewComment(
            commit_id=2,
            reviewer_id=1,
            content="Different commit"
        )
        
        await repository.create(comment1)
        await repository.create(comment2)
        await repository.create(comment3)
        
        comments = await repository.get_by_commit_and_reviewer(1, 1)
        
        assert len(comments) == 1
        assert comments[0].content == "Target comment"
    
    async def test_get_by_file_path(self, repository):
        """Test retrieving review comments by file path."""
        comment1 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            file_path="src/main.py",
            content="Main file comment"
        )
        comment2 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            file_path="src/utils.py",
            content="Utils file comment"
        )
        
        await repository.create(comment1)
        await repository.create(comment2)
        
        comments = await repository.get_by_file_path(1, "src/main.py")
        
        assert len(comments) == 1
        assert comments[0].content == "Main file comment"
    
    async def test_get_line_comments(self, repository):
        """Test retrieving line-specific comments."""
        comment1 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            file_path="src/main.py",
            line_number=42,
            content="Line 42 comment"
        )
        comment2 = ReviewComment(
            commit_id=1,
            reviewer_id=1,
            file_path="src/main.py",
            line_number=50,
            content="Line 50 comment"
        )
        
        await repository.create(comment1)
        await repository.create(comment2)
        
        comments = await repository.get_line_comments(1, "src/main.py", 42)
        
        assert len(comments) == 1
        assert comments[0].content == "Line 42 comment"
    
    async def test_update_review_comment(self, repository, sample_comment):
        """Test updating a review comment."""
        created = await repository.create(sample_comment)
        
        updated_comment = created.update_content("Updated comment content")
        result = await repository.update(updated_comment)
        
        assert result.content == "Updated comment content"
        assert result.updated_at is not None
    
    async def test_delete_review_comment(self, repository, sample_comment):
        """Test deleting a review comment."""
        created = await repository.create(sample_comment)
        
        success = await repository.delete(created.id)
        assert success is True
        
        # Verify it's gone
        retrieved = await repository.get_by_id(created.id)
        assert retrieved is None


class TestSqlAlchemyCommitReviewRepository:
    """Test SqlAlchemyCommitReviewRepository."""
    
    @pytest.fixture
    async def repository(self, db_session: AsyncSession):
        """Create repository instance."""
        return SqlAlchemyCommitReviewRepository(db_session)
    
    @pytest.fixture
    async def sample_review(self):
        """Create a sample commit review."""
        return CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
    
    async def test_create_commit_review(self, repository, sample_review):
        """Test creating a commit review."""
        created = await repository.create(sample_review)
        
        assert created.id is not None
        assert created.commit_id == sample_review.commit_id
        assert created.reviewer_id == sample_review.reviewer_id
        assert created.status == sample_review.status
        assert isinstance(created.created_at, datetime)
    
    async def test_get_by_id(self, repository, sample_review):
        """Test retrieving a commit review by ID."""
        created = await repository.create(sample_review)
        
        retrieved = await repository.get_by_id(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.status == created.status
    
    async def test_get_by_commit_id(self, repository):
        """Test retrieving reviews by commit ID."""
        review1 = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        review2 = CommitReview(
            commit_id=1,
            reviewer_id=2,
            status=CommitReview.ReviewStatus.APPROVED
        )
        review3 = CommitReview(
            commit_id=2,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        await repository.create(review1)
        await repository.create(review2)
        await repository.create(review3)
        
        reviews = await repository.get_by_commit_id(1)
        
        assert len(reviews) == 2
        assert all(r.commit_id == 1 for r in reviews)
    
    async def test_get_by_commit_and_reviewer(self, repository):
        """Test retrieving review by commit and reviewer."""
        review = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        await repository.create(review)
        
        retrieved = await repository.get_by_commit_and_reviewer(1, 1)
        
        assert retrieved is not None
        assert retrieved.commit_id == 1
        assert retrieved.reviewer_id == 1
    
    async def test_get_by_status(self, repository):
        """Test retrieving reviews by status."""
        review1 = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        review2 = CommitReview(
            commit_id=2,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.APPROVED
        )
        review3 = CommitReview(
            commit_id=3,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        await repository.create(review1)
        await repository.create(review2)
        await repository.create(review3)
        
        pending_reviews = await repository.get_by_status(CommitReview.ReviewStatus.PENDING)
        
        assert len(pending_reviews) == 2
        assert all(r.status == CommitReview.ReviewStatus.PENDING for r in pending_reviews)
    
    async def test_get_pending_reviews(self, repository):
        """Test retrieving pending reviews."""
        review1 = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        review2 = CommitReview(
            commit_id=2,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.APPROVED
        )
        
        await repository.create(review1)
        await repository.create(review2)
        
        pending = await repository.get_pending_reviews()
        
        assert len(pending) == 1
        assert pending[0].status == CommitReview.ReviewStatus.PENDING
    
    async def test_get_completed_reviews(self, repository):
        """Test retrieving completed reviews."""
        review1 = CommitReview(
            commit_id=1,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.APPROVED
        )
        review2 = CommitReview(
            commit_id=2,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.NEEDS_REVISION
        )
        review3 = CommitReview(
            commit_id=3,
            reviewer_id=1,
            status=CommitReview.ReviewStatus.PENDING
        )
        
        # Complete the first two reviews
        completed1 = review1.complete_review(CommitReview.ReviewStatus.APPROVED)
        completed2 = review2.complete_review(CommitReview.ReviewStatus.NEEDS_REVISION)
        
        await repository.create(completed1)
        await repository.create(completed2)
        await repository.create(review3)
        
        completed = await repository.get_completed_reviews()
        
        assert len(completed) == 2
        assert all(r.is_completed for r in completed)
    
    async def test_update_commit_review(self, repository, sample_review):
        """Test updating a commit review."""
        created = await repository.create(sample_review)
        
        updated_review = created.complete_review(CommitReview.ReviewStatus.APPROVED)
        result = await repository.update(updated_review)
        
        assert result.status == CommitReview.ReviewStatus.APPROVED
        assert result.reviewed_at is not None
    
    async def test_delete_commit_review(self, repository, sample_review):
        """Test deleting a commit review."""
        created = await repository.create(sample_review)
        
        success = await repository.delete(created.id)
        assert success is True
        
        # Verify it's gone
        retrieved = await repository.get_by_id(created.id)
        assert retrieved is None