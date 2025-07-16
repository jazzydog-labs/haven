# Implement Repository Domain Entity for TTR System

## Description
Create the Repository domain entity to represent Git repositories being tracked by the TTR system.

## Acceptance Criteria
- [ ] Repository domain entity created with validation
- [ ] Support for both local and remote repositories
- [ ] Unit tests for Repository entity
- [ ] Integration with existing Git operations

## Implementation Details

### Domain Entity
Location: `src/haven/domain/entities/repository.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from pathlib import Path

@dataclass
class Repository:
    name: str
    full_name: str
    url: str
    branch: str
    description: Optional[str] = None
    is_local: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Repository name cannot be empty")
        if not self.url:
            raise ValueError("Repository URL cannot be empty")
        if not self.branch:
            raise ValueError("Branch cannot be empty")
        
        # Validate URL format for local repositories
        if self.is_local:
            if not Path(self.url).exists():
                raise ValueError(f"Local repository path does not exist: {self.url}")
    
    @property
    def display_name(self) -> str:
        """Get display name for UI"""
        return self.full_name or self.name
    
    @property
    def is_github(self) -> bool:
        """Check if this is a GitHub repository"""
        return "github.com" in self.url.lower()
```

### Database Model
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

## Repository Service
Location: `src/haven/application/services/repository_service.py`

```python
from haven.domain.entities.repository import Repository
from haven.infrastructure.git.git_service import GitService

class RepositoryService:
    def __init__(self, git_service: GitService):
        self.git_service = git_service
    
    def validate_repository(self, repository: Repository) -> bool:
        """Validate that repository exists and is accessible"""
        if repository.is_local:
            return self.git_service.is_git_repository(repository.url)
        else:
            # TODO: Add remote repository validation
            return True
    
    def get_repository_info(self, path: str) -> dict:
        """Get repository information from Git"""
        return self.git_service.get_repository_info(path)
    
    def sync_commits(self, repository: Repository) -> list:
        """Sync commits from Git repository"""
        return self.git_service.get_commits(repository.url, repository.branch)
```

## Migration
```bash
just database::make "create_repositories_table"
```

## Tests
Location: `tests/unit/domain/entities/test_repository.py`

```python
import pytest
from haven.domain.entities.repository import Repository

def test_repository_creation():
    repo = Repository(
        name="haven",
        full_name="jazzydog-labs/haven",
        url="/Users/paul/dev/jazzydog-labs/haven",
        branch="main",
        description="Haven repository",
        is_local=True
    )
    assert repo.name == "haven"
    assert repo.branch == "main"
    assert repo.is_local is True

def test_repository_validation():
    with pytest.raises(ValueError, match="Repository name cannot be empty"):
        Repository(name="", full_name="test", url="/path", branch="main")
    
    with pytest.raises(ValueError, match="Branch cannot be empty"):
        Repository(name="test", full_name="test", url="/path", branch="")

def test_display_name_property():
    repo = Repository(
        name="haven",
        full_name="jazzydog-labs/haven",
        url="/path",
        branch="main"
    )
    assert repo.display_name == "jazzydog-labs/haven"

def test_is_github_property():
    github_repo = Repository(
        name="test",
        full_name="user/test",
        url="https://github.com/user/test.git",
        branch="main",
        is_local=False
    )
    assert github_repo.is_github is True
```

## Definition of Done
- [ ] Repository entity implemented with validation
- [ ] Database model created
- [ ] Migration created and applied
- [ ] Repository service created
- [ ] Unit tests written and passing
- [ ] Integration tests for Git operations
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added