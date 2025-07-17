"""Tests for review repository implementations."""

import pytest
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from haven.domain.entities.review_comment import ReviewComment, CommitReview
from haven.infrastructure.database.repositories.review_repository import (
    SqlAlchemyReviewCommentRepository,
    SqlAlchemyCommitReviewRepository
)


@pytest.mark.asyncio
async def test_create_review_comment(test_session: AsyncSession):
    """Test creating a review comment."""
    repository = SqlAlchemyReviewCommentRepository(test_session)
    
    comment = ReviewComment(
        commit_id=1,
        reviewer_id=1,
        line_number=42,
        file_path="src/main.py",
        content="Consider adding error handling here."
    )
    
    created = await repository.create(comment)
    
    assert created.id is not None
    assert created.commit_id == comment.commit_id
    assert created.reviewer_id == comment.reviewer_id
    assert created.content == comment.content
    assert isinstance(created.created_at, datetime)


@pytest.mark.asyncio
async def test_get_review_comment_by_id(test_session: AsyncSession):
    """Test retrieving a review comment by ID."""
    repository = SqlAlchemyReviewCommentRepository(test_session)
    
    comment = ReviewComment(
        commit_id=1,
        reviewer_id=1,
        content="Test comment"
    )
    
    created = await repository.create(comment)
    retrieved = await repository.get_by_id(created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.content == created.content


@pytest.mark.asyncio 
async def test_get_review_comment_by_id_not_found(test_session: AsyncSession):
    """Test retrieving a non-existent review comment."""
    repository = SqlAlchemyReviewCommentRepository(test_session)
    
    result = await repository.get_by_id(99999)
    assert result is None


@pytest.mark.asyncio
async def test_get_review_comments_by_commit_id(test_session: AsyncSession):
    """Test retrieving review comments by commit ID."""
    repository = SqlAlchemyReviewCommentRepository(test_session)
    
    comment1 = ReviewComment(commit_id=1, reviewer_id=1, content="First comment")
    comment2 = ReviewComment(commit_id=1, reviewer_id=2, content="Second comment") 
    comment3 = ReviewComment(commit_id=2, reviewer_id=1, content="Different commit")
    
    await repository.create(comment1)
    await repository.create(comment2)
    await repository.create(comment3)
    
    comments = await repository.get_by_commit_id(1)
    
    assert len(comments) == 2
    assert all(c.commit_id == 1 for c in comments)


@pytest.mark.asyncio
async def test_create_commit_review(test_session: AsyncSession):
    """Test creating a commit review."""
    repository = SqlAlchemyCommitReviewRepository(test_session)
    
    review = CommitReview(
        commit_id=1,
        reviewer_id=1,
        status=CommitReview.ReviewStatus.PENDING
    )
    
    created = await repository.create(review)
    
    assert created.id is not None
    assert created.commit_id == review.commit_id
    assert created.reviewer_id == review.reviewer_id
    assert created.status == review.status
    assert isinstance(created.created_at, datetime)


@pytest.mark.asyncio
async def test_get_commit_review_by_id(test_session: AsyncSession):
    """Test retrieving a commit review by ID."""
    repository = SqlAlchemyCommitReviewRepository(test_session)
    
    review = CommitReview(
        commit_id=1,
        reviewer_id=1,
        status=CommitReview.ReviewStatus.PENDING
    )
    
    created = await repository.create(review)
    retrieved = await repository.get_by_id(created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.status == created.status


@pytest.mark.asyncio
async def test_update_commit_review_status(test_session: AsyncSession):
    """Test updating a commit review status."""
    repository = SqlAlchemyCommitReviewRepository(test_session)
    
    review = CommitReview(
        commit_id=1,
        reviewer_id=1,
        status=CommitReview.ReviewStatus.PENDING
    )
    
    created = await repository.create(review)
    updated_review = created.complete_review(CommitReview.ReviewStatus.APPROVED)
    result = await repository.update(updated_review)
    
    assert result.status == CommitReview.ReviewStatus.APPROVED
    assert result.reviewed_at is not None