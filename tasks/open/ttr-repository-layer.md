# Implement TTR Repository Layer

## Description
Create the repository layer implementing the Clean Architecture pattern for all TTR entities, providing data access abstractions.

## Acceptance Criteria
- [ ] Repository interfaces defined in domain layer
- [ ] SQLAlchemy implementations in infrastructure layer
- [ ] Proper error handling and validation
- [ ] Unit tests for all repository operations
- [ ] Integration with existing database patterns

## Implementation Details

### Repository Interfaces

#### User Repository Interface
Location: `src/haven/domain/repositories/user_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from haven.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[User]:
        """Get all users"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        pass
```

#### Repository Repository Interface
Location: `src/haven/domain/repositories/repository_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from haven.domain.entities.repository import Repository

class RepositoryRepository(ABC):
    @abstractmethod
    async def create(self, repository: Repository) -> Repository:
        """Create a new repository"""
        pass
    
    @abstractmethod
    async def get_by_id(self, repo_id: int) -> Optional[Repository]:
        """Get repository by ID"""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Repository]:
        """Get repository by name"""
        pass
    
    @abstractmethod
    async def get_by_url(self, url: str) -> Optional[Repository]:
        """Get repository by URL"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Repository]:
        """Get all repositories"""
        pass
    
    @abstractmethod
    async def update(self, repository: Repository) -> Repository:
        """Update existing repository"""
        pass
    
    @abstractmethod
    async def delete(self, repo_id: int) -> bool:
        """Delete repository"""
        pass
```

#### Commit Repository Interface
Location: `src/haven/domain/repositories/commit_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from haven.domain.entities.commit import Commit, CommitReview, ReviewStatus

class CommitRepository(ABC):
    @abstractmethod
    async def create(self, commit: Commit) -> Commit:
        """Create a new commit"""
        pass
    
    @abstractmethod
    async def get_by_id(self, commit_id: int) -> Optional[Commit]:
        """Get commit by ID"""
        pass
    
    @abstractmethod
    async def get_by_hash(self, repository_id: int, commit_hash: str) -> Optional[Commit]:
        """Get commit by hash within repository"""
        pass
    
    @abstractmethod
    async def get_by_repository_id(self, repository_id: int, limit: int = 50) -> List[Commit]:
        """Get commits for a repository"""
        pass
    
    @abstractmethod
    async def get_pending_reviews(self, reviewer_id: int) -> List[Commit]:
        """Get commits pending review by user"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: ReviewStatus) -> List[Commit]:
        """Get commits by review status"""
        pass
    
    @abstractmethod
    async def update(self, commit: Commit) -> Commit:
        """Update existing commit"""
        pass
    
    @abstractmethod
    async def delete(self, commit_id: int) -> bool:
        """Delete commit"""
        pass
    
    @abstractmethod
    async def upsert(self, commit: Commit) -> Commit:
        """Insert or update commit (for sync operations)"""
        pass

class CommitReviewRepository(ABC):
    @abstractmethod
    async def create(self, review: CommitReview) -> CommitReview:
        """Create a new review"""
        pass
    
    @abstractmethod
    async def get_by_id(self, review_id: int) -> Optional[CommitReview]:
        """Get review by ID"""
        pass
    
    @abstractmethod
    async def get_by_commit_id(self, commit_id: int) -> Optional[CommitReview]:
        """Get review for a commit"""
        pass
    
    @abstractmethod
    async def get_by_reviewer_id(self, reviewer_id: int) -> List[CommitReview]:
        """Get reviews by reviewer"""
        pass
    
    @abstractmethod
    async def update(self, review: CommitReview) -> CommitReview:
        """Update existing review"""
        pass
    
    @abstractmethod
    async def delete(self, review_id: int) -> bool:
        """Delete review"""
        pass
```

#### Comment Repository Interface
Location: `src/haven/domain/repositories/comment_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from haven.domain.entities.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        """Create a new comment"""
        pass
    
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by ID"""
        pass
    
    @abstractmethod
    async def get_by_commit_id(self, commit_id: int) -> List[Comment]:
        """Get all comments for a commit"""
        pass
    
    @abstractmethod
    async def get_by_line(self, commit_id: int, file_path: str, line_number: int) -> List[Comment]:
        """Get comments for specific line"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Comment]:
        """Get all comments by user"""
        pass
    
    @abstractmethod
    async def update(self, comment: Comment) -> Comment:
        """Update existing comment"""
        pass
    
    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        """Delete comment"""
        pass
```

### SQLAlchemy Implementations

#### User Repository Implementation
Location: `src/haven/infrastructure/database/repositories/user_repository_impl.py`

```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from haven.domain.entities.user import User
from haven.domain.repositories.user_repository import UserRepository
from haven.infrastructure.database.models.user import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url
        )
        
        try:
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return self._to_entity(db_user)
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Username or email already exists")
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def get_all(self) -> List[User]:
        """Get all users"""
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [self._to_entity(db_user) for db_user in db_users]
    
    async def update(self, user: User) -> User:
        """Update existing user"""
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")
        
        db_user.username = user.username
        db_user.email = user.email
        db_user.display_name = user.display_name
        db_user.avatar_url = user.avatar_url
        
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return False
        
        await self.session.delete(db_user)
        await self.session.commit()
        return True
    
    def _to_entity(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            display_name=db_user.display_name,
            avatar_url=db_user.avatar_url,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
```

#### Commit Repository Implementation
Location: `src/haven/infrastructure/database/repositories/commit_repository_impl.py`

```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from haven.domain.entities.commit import Commit, CommitReview, ReviewStatus, DiffStats
from haven.domain.repositories.commit_repository import CommitRepository, CommitReviewRepository
from haven.infrastructure.database.models.commit import CommitModel, CommitReviewModel

class CommitRepositoryImpl(CommitRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, commit: Commit) -> Commit:
        """Create a new commit"""
        db_commit = CommitModel(
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
            deletions=commit.diff_stats.deletions
        )
        
        self.session.add(db_commit)
        await self.session.commit()
        await self.session.refresh(db_commit)
        return self._to_entity(db_commit)
    
    async def get_by_id(self, commit_id: int) -> Optional[Commit]:
        """Get commit by ID"""
        stmt = select(CommitModel).options(
            selectinload(CommitModel.review)
        ).where(CommitModel.id == commit_id)
        result = await self.session.execute(stmt)
        db_commit = result.scalar_one_or_none()
        return self._to_entity(db_commit) if db_commit else None
    
    async def get_by_hash(self, repository_id: int, commit_hash: str) -> Optional[Commit]:
        """Get commit by hash within repository"""
        stmt = select(CommitModel).options(
            selectinload(CommitModel.review)
        ).where(and_(
            CommitModel.repository_id == repository_id,
            CommitModel.commit_hash == commit_hash
        ))
        result = await self.session.execute(stmt)
        db_commit = result.scalar_one_or_none()
        return self._to_entity(db_commit) if db_commit else None
    
    async def get_by_repository_id(self, repository_id: int, limit: int = 50) -> List[Commit]:
        """Get commits for a repository"""
        stmt = select(CommitModel).options(
            selectinload(CommitModel.review)
        ).where(
            CommitModel.repository_id == repository_id
        ).order_by(CommitModel.committed_at.desc()).limit(limit)
        
        result = await self.session.execute(stmt)
        db_commits = result.scalars().all()
        return [self._to_entity(db_commit) for db_commit in db_commits]
    
    async def get_pending_reviews(self, reviewer_id: int) -> List[Commit]:
        """Get commits pending review by user"""
        stmt = select(CommitModel).join(CommitReviewModel).where(and_(
            CommitReviewModel.reviewer_id == reviewer_id,
            CommitReviewModel.status == ReviewStatus.PENDING_REVIEW
        ))
        
        result = await self.session.execute(stmt)
        db_commits = result.scalars().all()
        return [self._to_entity(db_commit) for db_commit in db_commits]
    
    async def upsert(self, commit: Commit) -> Commit:
        """Insert or update commit (for sync operations)"""
        existing = await self.get_by_hash(commit.repository_id, commit.commit_hash)
        
        if existing:
            existing.message = commit.message
            existing.diff_stats = commit.diff_stats
            return await self.update(existing)
        else:
            return await self.create(commit)
    
    def _to_entity(self, db_commit: CommitModel) -> Commit:
        """Convert database model to domain entity"""
        return Commit(
            id=db_commit.id,
            repository_id=db_commit.repository_id,
            commit_hash=db_commit.commit_hash,
            message=db_commit.message,
            author_name=db_commit.author_name,
            author_email=db_commit.author_email,
            committer_name=db_commit.committer_name,
            committer_email=db_commit.committer_email,
            committed_at=db_commit.committed_at,
            diff_stats=DiffStats(
                files_changed=db_commit.files_changed,
                insertions=db_commit.insertions,
                deletions=db_commit.deletions
            ),
            created_at=db_commit.created_at,
            updated_at=db_commit.updated_at
        )
```

### Repository Factory
Location: `src/haven/infrastructure/database/repositories/factory.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession
from haven.domain.repositories.user_repository import UserRepository
from haven.domain.repositories.repository_repository import RepositoryRepository
from haven.domain.repositories.commit_repository import CommitRepository, CommitReviewRepository
from haven.domain.repositories.comment_repository import CommentRepository
from .user_repository_impl import UserRepositoryImpl
from .repository_repository_impl import RepositoryRepositoryImpl
from .commit_repository_impl import CommitRepositoryImpl, CommitReviewRepositoryImpl
from .comment_repository_impl import CommentRepositoryImpl

class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def get_user_repository(self) -> UserRepository:
        return UserRepositoryImpl(self.session)
    
    def get_repository_repository(self) -> RepositoryRepository:
        return RepositoryRepositoryImpl(self.session)
    
    def get_commit_repository(self) -> CommitRepository:
        return CommitRepositoryImpl(self.session)
    
    def get_commit_review_repository(self) -> CommitReviewRepository:
        return CommitReviewRepositoryImpl(self.session)
    
    def get_comment_repository(self) -> CommentRepository:
        return CommentRepositoryImpl(self.session)
```

## Error Handling

### Custom Exceptions
Location: `src/haven/domain/exceptions/repository_exceptions.py`

```python
class RepositoryException(Exception):
    """Base exception for repository operations"""
    pass

class EntityNotFoundException(RepositoryException):
    """Raised when entity is not found"""
    pass

class DuplicateEntityException(RepositoryException):
    """Raised when trying to create duplicate entity"""
    pass

class ValidationException(RepositoryException):
    """Raised when entity validation fails"""
    pass
```

## Testing

### Unit Tests
Location: `tests/unit/infrastructure/database/repositories/test_user_repository_impl.py`

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from haven.domain.entities.user import User
from haven.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl

@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    repo = UserRepositoryImpl(async_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    created_user = await repo.create(user)
    
    assert created_user.id is not None
    assert created_user.username == "testuser"
    assert created_user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_user_by_username(async_session: AsyncSession):
    repo = UserRepositoryImpl(async_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    await repo.create(user)
    found_user = await repo.get_by_username("testuser")
    
    assert found_user is not None
    assert found_user.username == "testuser"

@pytest.mark.asyncio
async def test_duplicate_username_raises_error(async_session: AsyncSession):
    repo = UserRepositoryImpl(async_session)
    
    user1 = User(username="testuser", email="test1@example.com", display_name="Test User 1")
    user2 = User(username="testuser", email="test2@example.com", display_name="Test User 2")
    
    await repo.create(user1)
    
    with pytest.raises(ValueError, match="Username or email already exists"):
        await repo.create(user2)
```

### Integration Tests
Location: `tests/integration/repositories/test_commit_repository_integration.py`

```python
import pytest
from haven.domain.entities.commit import Commit, DiffStats
from haven.infrastructure.database.repositories.commit_repository_impl import CommitRepositoryImpl
from datetime import datetime

@pytest.mark.asyncio
async def test_commit_upsert_operation(async_session, sample_repository):
    repo = CommitRepositoryImpl(async_session)
    
    commit = Commit(
        repository_id=sample_repository.id,
        commit_hash="abc123",
        message="Initial commit",
        author_name="Test Author",
        author_email="author@example.com",
        committer_name="Test Author",
        committer_email="author@example.com",
        committed_at=datetime.utcnow(),
        diff_stats=DiffStats(files_changed=1, insertions=10, deletions=0)
    )
    
    # First upsert should create
    result1 = await repo.upsert(commit)
    assert result1.id is not None
    
    # Second upsert should update
    commit.message = "Updated commit message"
    result2 = await repo.upsert(commit)
    assert result2.id == result1.id
    assert result2.message == "Updated commit message"
```

## Definition of Done
- [ ] All repository interfaces implemented
- [ ] SQLAlchemy repository implementations created
- [ ] Repository factory created
- [ ] Error handling implemented
- [ ] Unit tests for all repositories
- [ ] Integration tests for complex operations
- [ ] Performance considerations addressed
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added