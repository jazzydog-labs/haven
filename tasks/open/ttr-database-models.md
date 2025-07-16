# Create TTR Database Models and Migrations

## Description
Create SQLAlchemy database models for the TTR system entities and generate Alembic migrations.

## Acceptance Criteria
- [ ] All TTR database models created
- [ ] Foreign key relationships properly defined
- [ ] Indexes added for performance
- [ ] Alembic migrations generated
- [ ] Database constraints and validations

## Implementation Details

### Database Models Structure
```
src/haven/infrastructure/database/models/
├── user.py           # User model
├── repository.py     # Repository model  
├── commit.py         # Commit and CommitReview models
├── comment.py        # Comment model
└── __init__.py       # Model imports
```

### User Model
Location: `src/haven/infrastructure/database/models/user.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from haven.infrastructure.database.base import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    comments = relationship("CommentModel", back_populates="user")
    reviews = relationship("CommitReviewModel", back_populates="reviewer")
```

### Repository Model
Location: `src/haven/infrastructure/database/models/repository.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from haven.infrastructure.database.base import Base

class RepositoryModel(Base):
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    branch = Column(String(255), nullable=False, default="main")
    description = Column(Text, nullable=True)
    is_local = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    commits = relationship("CommitModel", back_populates="repository")
```

### Commit Models
Location: `src/haven/infrastructure/database/models/commit.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, UniqueConstraint, Index
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
    
    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('repository_id', 'commit_hash', name='uq_repo_commit'),
        Index('idx_repository_committed_at', 'repository_id', 'committed_at'),
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
    
    # Indexes
    __table_args__ = (
        Index('idx_reviewer_status', 'reviewer_id', 'status'),
        Index('idx_commit_status', 'commit_id', 'status'),
    )
```

### Comment Model
Location: `src/haven/infrastructure/database/models/comment.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from haven.infrastructure.database.base import Base

class CommentModel(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    commit_id = Column(Integer, ForeignKey("commits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    line_number = Column(Integer, nullable=True)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    commit = relationship("CommitModel", back_populates="comments")
    user = relationship("UserModel", back_populates="comments")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_commit_user', 'commit_id', 'user_id'),
        Index('idx_commit_file_line', 'commit_id', 'file_path', 'line_number'),
    )
```

### Model Imports
Location: `src/haven/infrastructure/database/models/__init__.py`

```python
from .user import UserModel
from .repository import RepositoryModel
from .commit import CommitModel, CommitReviewModel
from .comment import CommentModel

__all__ = [
    "UserModel",
    "RepositoryModel", 
    "CommitModel",
    "CommitReviewModel",
    "CommentModel"
]
```

## Alembic Migrations

### Step 1: Create Migration Files
```bash
# Create users table
just database::make "create_users_table"

# Create repositories table
just database::make "create_repositories_table"

# Create commits and commit_reviews tables
just database::make "create_commits_and_reviews_tables"

# Create comments table
just database::make "create_comments_table"
```

### Step 2: Migration Content Examples

**Users Table Migration:**
```python
"""create_users_table

Revision ID: 001_create_users
Revises: 
Create Date: 2024-XX-XX
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String(50), nullable=False, index=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('avatar_url', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    
    op.create_unique_constraint('uq_users_username', 'users', ['username'])
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')
```

**Repositories Table Migration:**
```python
"""create_repositories_table

Revision ID: 002_create_repositories
Revises: 001_create_users
Create Date: 2024-XX-XX
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'repositories',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('url', sa.Text, nullable=False),
        sa.Column('branch', sa.String(255), nullable=False, default='main'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_local', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('repositories')
```

## Model Validation

### Tests
Location: `tests/unit/infrastructure/database/models/test_ttr_models.py`

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from haven.infrastructure.database.models import UserModel, RepositoryModel, CommitModel
from haven.infrastructure.database.base import Base

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_user_model_creation(db_session):
    user = UserModel(
        username="plva",
        email="paul@example.com",
        display_name="Paul"
    )
    
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == "plva"
    assert user.created_at is not None

def test_repository_model_relationships(db_session):
    repo = RepositoryModel(
        name="haven",
        full_name="jazzydog-labs/haven",
        url="/path/to/repo",
        branch="main"
    )
    
    db_session.add(repo)
    db_session.commit()
    
    assert repo.id is not None
    assert repo.commits == []
```

## Database Seeding

### Initial Data
Location: `src/haven/infrastructure/database/seed_data.py`

```python
from haven.infrastructure.database.models import UserModel, RepositoryModel

def seed_initial_data(session):
    """Seed initial data for development"""
    
    # Create default user
    user = UserModel(
        username="plva",
        email="paul@example.com",
        display_name="Paul"
    )
    session.add(user)
    
    # Create default repository
    repo = RepositoryModel(
        name="haven",
        full_name="jazzydog-labs/haven",
        url="/Users/paul/dev/jazzydog-labs/haven",
        branch="main",
        description="Haven repository",
        is_local=True
    )
    session.add(repo)
    
    session.commit()
    return user, repo
```

## Performance Considerations

### Indexes
- `users.username` - Unique index for fast lookups
- `users.email` - Unique index for authentication
- `repositories.name` - Index for repository searches
- `commits.commit_hash` - Index for Git hash lookups
- `commits.repository_id + committed_at` - Composite index for timeline queries
- `commit_reviews.reviewer_id + status` - Index for review dashboard
- `comments.commit_id + user_id` - Index for comment queries

### Constraints
- Unique constraint on `(repository_id, commit_hash)` to prevent duplicate commits
- Foreign key constraints with proper cascading
- NOT NULL constraints on required fields

## Definition of Done
- [ ] All database models implemented
- [ ] Foreign key relationships defined
- [ ] Indexes added for performance
- [ ] Alembic migrations created
- [ ] Migration files generated and tested
- [ ] Database constraints implemented
- [ ] Seed data created
- [ ] Unit tests for models
- [ ] Integration tests for relationships
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added