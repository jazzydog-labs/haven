# Implement Commit Domain Entity for TTR System

## Description
Create the Commit domain entity to represent Git commits within tracked repositories, including their review status and metadata.

## Acceptance Criteria
- [ ] Commit domain entity created with validation
- [ ] CommitReview entity for tracking review status
- [ ] Integration with existing Git operations
- [ ] Support for diff statistics and metadata

## Implementation Details

### Domain Entities
Location: `src/haven/domain/entities/commit.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class ReviewStatus(Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    DRAFT = "draft"

@dataclass
class DiffStats:
    files_changed: int
    insertions: int
    deletions: int
    
    @property
    def total_changes(self) -> int:
        return self.insertions + self.deletions

@dataclass
class Commit:
    repository_id: int
    commit_hash: str
    message: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    committed_at: datetime
    diff_stats: DiffStats
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.commit_hash:
            raise ValueError("Commit hash cannot be empty")
        if len(self.commit_hash) < 7:
            raise ValueError("Commit hash must be at least 7 characters")
        if not self.message:
            raise ValueError("Commit message cannot be empty")
        if not self.author_name:
            raise ValueError("Author name cannot be empty")
        if not self.author_email:
            raise ValueError("Author email cannot be empty")
    
    @property
    def short_hash(self) -> str:
        """Get short version of commit hash"""
        return self.commit_hash[:7]
    
    @property
    def short_message(self) -> str:
        """Get first line of commit message"""
        return self.message.split('\n')[0]

@dataclass
class CommitReview:
    commit_id: int
    reviewer_id: int
    status: ReviewStatus
    reviewed_at: Optional[datetime] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.status == ReviewStatus.APPROVED and not self.reviewed_at:
            self.reviewed_at = datetime.utcnow()
    
    def approve(self, reviewer_id: int):
        """Mark commit as approved"""
        self.status = ReviewStatus.APPROVED
        self.reviewer_id = reviewer_id
        self.reviewed_at = datetime.utcnow()
    
    def request_revision(self, reviewer_id: int):
        """Mark commit as needing revision"""
        self.status = ReviewStatus.NEEDS_REVISION
        self.reviewer_id = reviewer_id
        self.reviewed_at = datetime.utcnow()
```

### Database Models
Location: `src/haven/infrastructure/database/models/commit.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from haven.infrastructure.database.base import Base
from haven.domain.entities.commit import ReviewStatus

class CommitModel(Base):
    __tablename__ = "commits"
    
    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    commit_hash = Column(String(40), nullable=False, index=True)
    message = Column(Text, nullable=False)
    author_name = Column(String(255), nullable=False)
    author_email = Column(String(255), nullable=False)
    committer_name = Column(String(255), nullable=False)
    committer_email = Column(String(255), nullable=False)
    committed_at = Column(DateTime, nullable=False)
    
    # Diff statistics
    files_changed = Column(Integer, nullable=False, default=0)
    insertions = Column(Integer, nullable=False, default=0)
    deletions = Column(Integer, nullable=False, default=0)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    repository = relationship("RepositoryModel", back_populates="commits")
    review = relationship("CommitReviewModel", back_populates="commit", uselist=False)
    comments = relationship("CommentModel", back_populates="commit")
    
    # Unique constraint on repository_id + commit_hash
    __table_args__ = (
        UniqueConstraint('repository_id', 'commit_hash', name='uq_repo_commit'),
    )

class CommitReviewModel(Base):
    __tablename__ = "commit_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    commit_id = Column(Integer, ForeignKey("commits.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ReviewStatus), nullable=False, default=ReviewStatus.PENDING_REVIEW)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    commit = relationship("CommitModel", back_populates="review")
    reviewer = relationship("UserModel", back_populates="reviews")
    comments = relationship("CommentModel", back_populates="review")
```

## Application Service
Location: `src/haven/application/services/commit_service.py`

```python
from typing import List, Optional
from haven.domain.entities.commit import Commit, CommitReview, ReviewStatus, DiffStats
from haven.infrastructure.git.git_service import GitService

class CommitService:
    def __init__(self, git_service: GitService):
        self.git_service = git_service
    
    def sync_repository_commits(self, repository_id: int, repo_path: str, branch: str) -> List[Commit]:
        """Sync commits from Git repository"""
        git_commits = self.git_service.get_commits(repo_path, branch)
        commits = []
        
        for git_commit in git_commits:
            diff_stats = self.git_service.get_commit_stats(repo_path, git_commit['hash'])
            
            commit = Commit(
                repository_id=repository_id,
                commit_hash=git_commit['hash'],
                message=git_commit['message'],
                author_name=git_commit['author_name'],
                author_email=git_commit['author_email'],
                committer_name=git_commit['committer_name'],
                committer_email=git_commit['committer_email'],
                committed_at=git_commit['committed_at'],
                diff_stats=DiffStats(
                    files_changed=diff_stats['files_changed'],
                    insertions=diff_stats['insertions'],
                    deletions=diff_stats['deletions']
                )
            )
            commits.append(commit)
        
        return commits
    
    def create_review(self, commit_id: int, reviewer_id: int) -> CommitReview:
        """Create a new review for a commit"""
        return CommitReview(
            commit_id=commit_id,
            reviewer_id=reviewer_id,
            status=ReviewStatus.PENDING_REVIEW
        )
    
    def update_review_status(self, review: CommitReview, status: ReviewStatus, reviewer_id: int) -> CommitReview:
        """Update review status"""
        if status == ReviewStatus.APPROVED:
            review.approve(reviewer_id)
        elif status == ReviewStatus.NEEDS_REVISION:
            review.request_revision(reviewer_id)
        else:
            review.status = status
            review.reviewer_id = reviewer_id
        
        return review
```

## Migration
```bash
just db-make "create_commits_and_reviews_tables"
```

## Tests
Location: `tests/unit/domain/entities/test_commit.py`

```python
import pytest
from datetime import datetime
from haven.domain.entities.commit import Commit, CommitReview, ReviewStatus, DiffStats

def test_commit_creation():
    diff_stats = DiffStats(files_changed=2, insertions=10, deletions=5)
    commit = Commit(
        repository_id=1,
        commit_hash="abc123def456",
        message="Add new feature",
        author_name="Paul",
        author_email="paul@example.com",
        committer_name="Paul",
        committer_email="paul@example.com",
        committed_at=datetime.utcnow(),
        diff_stats=diff_stats
    )
    
    assert commit.repository_id == 1
    assert commit.short_hash == "abc123d"
    assert commit.short_message == "Add new feature"

def test_commit_validation():
    diff_stats = DiffStats(files_changed=1, insertions=5, deletions=2)
    
    with pytest.raises(ValueError, match="Commit hash cannot be empty"):
        Commit(
            repository_id=1,
            commit_hash="",
            message="Test",
            author_name="Paul",
            author_email="paul@example.com",
            committer_name="Paul",
            committer_email="paul@example.com",
            committed_at=datetime.utcnow(),
            diff_stats=diff_stats
        )

def test_commit_review_creation():
    review = CommitReview(
        commit_id=1,
        reviewer_id=1,
        status=ReviewStatus.PENDING_REVIEW
    )
    
    assert review.status == ReviewStatus.PENDING_REVIEW
    assert review.reviewed_at is None

def test_commit_review_approval():
    review = CommitReview(
        commit_id=1,
        reviewer_id=1,
        status=ReviewStatus.PENDING_REVIEW
    )
    
    review.approve(1)
    assert review.status == ReviewStatus.APPROVED
    assert review.reviewed_at is not None

def test_diff_stats():
    stats = DiffStats(files_changed=3, insertions=15, deletions=8)
    assert stats.total_changes == 23
```

## Definition of Done
- [ ] Commit and CommitReview entities implemented
- [ ] Database models created
- [ ] Migration created and applied
- [ ] Commit service created
- [ ] Unit tests written and passing
- [ ] Integration tests for Git operations
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added