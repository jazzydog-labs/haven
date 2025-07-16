# Implement Comment Domain Entity for TTR System

## Description
Create the Comment domain entity to represent comments made on commits during the review process, including support for line-specific comments.

## Acceptance Criteria
- [ ] Comment domain entity created with validation
- [ ] Support for general and line-specific comments
- [ ] Unit tests for Comment entity
- [ ] Integration with commit review system

## Implementation Details

### Domain Entity
Location: `src/haven/domain/entities/comment.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Comment:
    commit_id: int
    user_id: int
    content: str
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.content or not self.content.strip():
            raise ValueError("Comment content cannot be empty")
        if self.line_number is not None and self.line_number < 1:
            raise ValueError("Line number must be positive")
        if self.line_number is not None and not self.file_path:
            raise ValueError("File path is required for line-specific comments")
    
    @property
    def is_line_specific(self) -> bool:
        """Check if this is a line-specific comment"""
        return self.line_number is not None and self.file_path is not None
    
    @property
    def is_general(self) -> bool:
        """Check if this is a general commit comment"""
        return not self.is_line_specific
    
    @property
    def preview(self) -> str:
        """Get preview of comment content (first 100 characters)"""
        if len(self.content) <= 100:
            return self.content
        return self.content[:97] + "..."
    
    def update_content(self, new_content: str):
        """Update comment content with validation"""
        if not new_content or not new_content.strip():
            raise ValueError("Comment content cannot be empty")
        self.content = new_content.strip()
        self.updated_at = datetime.utcnow()
```

### Database Model
Location: `src/haven/infrastructure/database/models/comment.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
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

## Application Service
Location: `src/haven/application/services/comment_service.py`

```python
from typing import List, Optional
from haven.domain.entities.comment import Comment

class CommentService:
    def __init__(self, comment_repository):
        self.comment_repository = comment_repository
    
    def create_comment(self, commit_id: int, user_id: int, content: str, 
                      line_number: Optional[int] = None, 
                      file_path: Optional[str] = None) -> Comment:
        """Create a new comment"""
        comment = Comment(
            commit_id=commit_id,
            user_id=user_id,
            content=content.strip(),
            line_number=line_number,
            file_path=file_path
        )
        
        return self.comment_repository.create(comment)
    
    def update_comment(self, comment_id: int, user_id: int, new_content: str) -> Comment:
        """Update existing comment (only by original author)"""
        comment = self.comment_repository.get_by_id(comment_id)
        
        if comment.user_id != user_id:
            raise ValueError("Only the comment author can update the comment")
        
        comment.update_content(new_content)
        return self.comment_repository.update(comment)
    
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        """Delete comment (only by original author)"""
        comment = self.comment_repository.get_by_id(comment_id)
        
        if comment.user_id != user_id:
            raise ValueError("Only the comment author can delete the comment")
        
        return self.comment_repository.delete(comment_id)
    
    def get_commit_comments(self, commit_id: int) -> List[Comment]:
        """Get all comments for a commit"""
        return self.comment_repository.get_by_commit_id(commit_id)
    
    def get_line_comments(self, commit_id: int, file_path: str, line_number: int) -> List[Comment]:
        """Get comments for a specific line in a file"""
        return self.comment_repository.get_by_line(commit_id, file_path, line_number)
    
    def get_user_comments(self, user_id: int) -> List[Comment]:
        """Get all comments by a user"""
        return self.comment_repository.get_by_user_id(user_id)
```

## Repository Interface
Location: `src/haven/domain/repositories/comment_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from haven.domain.entities.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    def create(self, comment: Comment) -> Comment:
        """Create a new comment"""
        pass
    
    @abstractmethod
    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by ID"""
        pass
    
    @abstractmethod
    def update(self, comment: Comment) -> Comment:
        """Update existing comment"""
        pass
    
    @abstractmethod
    def delete(self, comment_id: int) -> bool:
        """Delete comment"""
        pass
    
    @abstractmethod
    def get_by_commit_id(self, commit_id: int) -> List[Comment]:
        """Get all comments for a commit"""
        pass
    
    @abstractmethod
    def get_by_line(self, commit_id: int, file_path: str, line_number: int) -> List[Comment]:
        """Get comments for specific line"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Comment]:
        """Get all comments by user"""
        pass
```

## Migration
```bash
just database::make "create_comments_table"
```

## Tests
Location: `tests/unit/domain/entities/test_comment.py`

```python
import pytest
from datetime import datetime
from haven.domain.entities.comment import Comment

def test_comment_creation():
    comment = Comment(
        commit_id=1,
        user_id=1,
        content="This looks good!"
    )
    
    assert comment.commit_id == 1
    assert comment.user_id == 1
    assert comment.content == "This looks good!"
    assert comment.is_general is True
    assert comment.is_line_specific is False

def test_line_specific_comment():
    comment = Comment(
        commit_id=1,
        user_id=1,
        content="Fix this line",
        line_number=42,
        file_path="src/main.py"
    )
    
    assert comment.is_line_specific is True
    assert comment.is_general is False
    assert comment.line_number == 42
    assert comment.file_path == "src/main.py"

def test_comment_validation():
    with pytest.raises(ValueError, match="Comment content cannot be empty"):
        Comment(commit_id=1, user_id=1, content="")
    
    with pytest.raises(ValueError, match="Comment content cannot be empty"):
        Comment(commit_id=1, user_id=1, content="   ")
    
    with pytest.raises(ValueError, match="Line number must be positive"):
        Comment(commit_id=1, user_id=1, content="Test", line_number=0)
    
    with pytest.raises(ValueError, match="File path is required for line-specific comments"):
        Comment(commit_id=1, user_id=1, content="Test", line_number=5)

def test_comment_preview():
    short_comment = Comment(commit_id=1, user_id=1, content="Short")
    assert short_comment.preview == "Short"
    
    long_content = "This is a very long comment that exceeds the preview limit and should be truncated"
    long_comment = Comment(commit_id=1, user_id=1, content=long_content)
    assert len(long_comment.preview) <= 100
    assert long_comment.preview.endswith("...")

def test_update_content():
    comment = Comment(commit_id=1, user_id=1, content="Original")
    comment.update_content("Updated content")
    
    assert comment.content == "Updated content"
    assert comment.updated_at is not None
    
    with pytest.raises(ValueError, match="Comment content cannot be empty"):
        comment.update_content("")
```

Location: `tests/unit/application/services/test_comment_service.py`

```python
import pytest
from unittest.mock import Mock
from haven.application.services.comment_service import CommentService
from haven.domain.entities.comment import Comment

def test_create_comment():
    mock_repo = Mock()
    service = CommentService(mock_repo)
    
    comment = Comment(commit_id=1, user_id=1, content="Test comment")
    mock_repo.create.return_value = comment
    
    result = service.create_comment(1, 1, "Test comment")
    
    assert result.content == "Test comment"
    mock_repo.create.assert_called_once()

def test_update_comment_authorization():
    mock_repo = Mock()
    service = CommentService(mock_repo)
    
    comment = Comment(commit_id=1, user_id=1, content="Original", id=1)
    mock_repo.get_by_id.return_value = comment
    
    # Should work for original author
    service.update_comment(1, 1, "Updated")
    
    # Should fail for different user
    with pytest.raises(ValueError, match="Only the comment author can update"):
        service.update_comment(1, 2, "Updated")

def test_delete_comment_authorization():
    mock_repo = Mock()
    service = CommentService(mock_repo)
    
    comment = Comment(commit_id=1, user_id=1, content="Test", id=1)
    mock_repo.get_by_id.return_value = comment
    
    # Should work for original author
    service.delete_comment(1, 1)
    
    # Should fail for different user
    with pytest.raises(ValueError, match="Only the comment author can delete"):
        service.delete_comment(1, 2)
```

## Definition of Done
- [ ] Comment entity implemented with validation
- [ ] Database model created
- [ ] Migration created and applied
- [ ] Comment service created
- [ ] Comment repository interface defined
- [ ] Unit tests written and passing
- [ ] Integration tests for comment operations
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added