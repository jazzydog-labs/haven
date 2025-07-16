# Implement User Domain Entity for TTR System

## Description
Create the User domain entity to represent users who can review commits and make comments in the TTR (Task, Todo, Review) system.

## Acceptance Criteria
- [ ] User domain entity created with proper validation
- [ ] Unit tests for User entity
- [ ] User dataclass/model follows domain-driven design
- [ ] Integration with existing Clean Architecture patterns

## Implementation Details

### Domain Entity
Location: `src/haven/domain/entities/user.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    username: str
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        # Validation logic
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
```

### Domain Rules
- Username must be unique
- Email must be valid format
- Display name defaults to username if not provided
- Avatar URL is optional

## Database Model
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

## Migration
Create Alembic migration for users table:

```bash
just database::make "create_users_table"
```

## Tests
Location: `tests/unit/domain/entities/test_user.py`

```python
import pytest
from haven.domain.entities.user import User

def test_user_creation():
    user = User(
        username="plva",
        email="paul@example.com",
        display_name="Paul"
    )
    assert user.username == "plva"
    assert user.email == "paul@example.com"
    assert user.display_name == "Paul"

def test_user_validation():
    with pytest.raises(ValueError, match="Username cannot be empty"):
        User(username="", email="test@example.com", display_name="Test")
    
    with pytest.raises(ValueError, match="Invalid email format"):
        User(username="test", email="invalid-email", display_name="Test")
```

## Definition of Done
- [ ] User entity implemented with validation
- [ ] Database model created
- [ ] Migration created and applied
- [ ] Unit tests written and passing
- [ ] Integration tests for database operations
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added