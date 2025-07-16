# Create TTR API Endpoints

## Description
Create RESTful API endpoints for the TTR system using FastAPI, following existing patterns and Clean Architecture principles.

## Acceptance Criteria
- [ ] REST API endpoints for all TTR entities
- [ ] Proper HTTP status codes and error handling
- [ ] Request/response models with validation
- [ ] Authentication and authorization
- [ ] API documentation with OpenAPI/Swagger
- [ ] Integration with existing FastAPI patterns

## Implementation Details

### API Structure
```
src/haven/interface/api/routes/
├── ttr/
│   ├── __init__.py
│   ├── users.py           # User management endpoints
│   ├── repositories.py    # Repository management endpoints
│   ├── commits.py         # Commit and review endpoints
│   └── comments.py        # Comment endpoints
└── main.py               # Route registration
```

### Request/Response Models
Location: `src/haven/interface/api/models/ttr/`

#### User Models
```python
# src/haven/interface/api/models/ttr/user_models.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    display_name: str
    avatar_url: Optional[str] = None

class UserUpdateRequest(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

#### Repository Models
```python
# src/haven/interface/api/models/ttr/repository_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RepositoryCreateRequest(BaseModel):
    name: str
    full_name: str
    url: str
    branch: str = "main"
    description: Optional[str] = None
    is_local: bool = True

class RepositoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    branch: Optional[str] = None
    description: Optional[str] = None

class RepositoryResponse(BaseModel):
    id: int
    name: str
    full_name: str
    url: str
    branch: str
    description: Optional[str] = None
    is_local: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RepositorySyncRequest(BaseModel):
    force: bool = False
```

#### Commit Models
```python
# src/haven/interface/api/models/ttr/commit_models.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ReviewStatusEnum(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    DRAFT = "draft"

class DiffStatsResponse(BaseModel):
    files_changed: int
    insertions: int
    deletions: int
    total_changes: int

class CommitResponse(BaseModel):
    id: int
    repository_id: int
    commit_hash: str
    message: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    committed_at: datetime
    diff_stats: DiffStatsResponse
    short_hash: str
    short_message: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommitReviewResponse(BaseModel):
    id: int
    commit_id: int
    reviewer_id: int
    status: ReviewStatusEnum
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommitReviewUpdateRequest(BaseModel):
    status: ReviewStatusEnum
    reviewer_id: int

class CommitListResponse(BaseModel):
    commits: List[CommitResponse]
    total: int
    page: int
    per_page: int
```

### API Endpoints

#### User Endpoints
Location: `src/haven/interface/api/routes/ttr/users.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from haven.interface.api.models.ttr.user_models import (
    UserCreateRequest, UserUpdateRequest, UserResponse
)
from haven.application.services.user_service import UserService
from haven.infrastructure.database.session import get_async_session
from haven.infrastructure.database.repositories.factory import RepositoryFactory

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new user"""
    factory = RepositoryFactory(db)
    user_service = UserService(factory.get_user_repository())
    
    try:
        user = await user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            display_name=user_data.display_name,
            avatar_url=user_data.avatar_url
        )
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_async_session)):
    """Get all users"""
    factory = RepositoryFactory(db)
    user_service = UserService(factory.get_user_repository())
    
    users = await user_service.get_all_users()
    return [UserResponse.from_orm(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get user by ID"""
    factory = RepositoryFactory(db)
    user_service = UserService(factory.get_user_repository())
    
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Update user"""
    factory = RepositoryFactory(db)
    user_service = UserService(factory.get_user_repository())
    
    try:
        user = await user_service.update_user(
            user_id=user_id,
            display_name=user_data.display_name,
            avatar_url=user_data.avatar_url
        )
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Delete user"""
    factory = RepositoryFactory(db)
    user_service = UserService(factory.get_user_repository())
    
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
```

#### Repository Endpoints
Location: `src/haven/interface/api/routes/ttr/repositories.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from haven.interface.api.models.ttr.repository_models import (
    RepositoryCreateRequest, RepositoryUpdateRequest, RepositoryResponse, RepositorySyncRequest
)
from haven.application.services.repository_service import RepositoryService
from haven.infrastructure.database.session import get_async_session
from haven.infrastructure.database.repositories.factory import RepositoryFactory

router = APIRouter(prefix="/repositories", tags=["repositories"])

@router.post("/", response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
async def create_repository(
    repo_data: RepositoryCreateRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new repository"""
    factory = RepositoryFactory(db)
    repo_service = RepositoryService(factory.get_repository_repository())
    
    try:
        repository = await repo_service.create_repository(
            name=repo_data.name,
            full_name=repo_data.full_name,
            url=repo_data.url,
            branch=repo_data.branch,
            description=repo_data.description,
            is_local=repo_data.is_local
        )
        return RepositoryResponse.from_orm(repository)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[RepositoryResponse])
async def get_repositories(db: AsyncSession = Depends(get_async_session)):
    """Get all repositories"""
    factory = RepositoryFactory(db)
    repo_service = RepositoryService(factory.get_repository_repository())
    
    repositories = await repo_service.get_all_repositories()
    return [RepositoryResponse.from_orm(repo) for repo in repositories]

@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get repository by ID"""
    factory = RepositoryFactory(db)
    repo_service = RepositoryService(factory.get_repository_repository())
    
    repository = await repo_service.get_repository_by_id(repo_id)
    if not repository:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    return RepositoryResponse.from_orm(repository)

@router.post("/{repo_id}/sync", status_code=status.HTTP_202_ACCEPTED)
async def sync_repository(
    repo_id: int,
    sync_data: RepositorySyncRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Sync repository commits from Git"""
    factory = RepositoryFactory(db)
    repo_service = RepositoryService(factory.get_repository_repository())
    
    try:
        result = await repo_service.sync_repository_commits(repo_id, sync_data.force)
        return {"message": f"Synced {result['commits_added']} commits", "details": result}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
```

#### Commit Endpoints
Location: `src/haven/interface/api/routes/ttr/commits.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from haven.interface.api.models.ttr.commit_models import (
    CommitResponse, CommitListResponse, CommitReviewResponse, 
    CommitReviewUpdateRequest, ReviewStatusEnum
)
from haven.application.services.commit_service import CommitService
from haven.application.services.commit_review_service import CommitReviewService
from haven.infrastructure.database.session import get_async_session
from haven.infrastructure.database.repositories.factory import RepositoryFactory

router = APIRouter(prefix="/commits", tags=["commits"])

@router.get("/", response_model=CommitListResponse)
async def get_commits(
    repository_id: Optional[int] = Query(None),
    status: Optional[ReviewStatusEnum] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    """Get commits with optional filtering"""
    factory = RepositoryFactory(db)
    commit_service = CommitService(factory.get_commit_repository())
    
    commits = await commit_service.get_commits(
        repository_id=repository_id,
        status=status,
        page=page,
        per_page=per_page
    )
    
    return CommitListResponse(
        commits=[CommitResponse.from_orm(commit) for commit in commits],
        total=len(commits),  # TODO: Implement proper pagination
        page=page,
        per_page=per_page
    )

@router.get("/{commit_id}", response_model=CommitResponse)
async def get_commit(
    commit_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get commit by ID"""
    factory = RepositoryFactory(db)
    commit_service = CommitService(factory.get_commit_repository())
    
    commit = await commit_service.get_commit_by_id(commit_id)
    if not commit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commit not found"
        )
    
    return CommitResponse.from_orm(commit)

@router.get("/{commit_id}/diff")
async def get_commit_diff(
    commit_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get commit diff using existing diff service"""
    factory = RepositoryFactory(db)
    commit_service = CommitService(factory.get_commit_repository())
    
    commit = await commit_service.get_commit_by_id(commit_id)
    if not commit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commit not found"
        )
    
    # Use existing diff service
    diff_content = await commit_service.get_commit_diff(commit_id)
    return {"diff": diff_content}

@router.post("/{commit_id}/review", response_model=CommitReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_commit_review(
    commit_id: int,
    reviewer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a review for a commit"""
    factory = RepositoryFactory(db)
    review_service = CommitReviewService(factory.get_commit_review_repository())
    
    try:
        review = await review_service.create_review(commit_id, reviewer_id)
        return CommitReviewResponse.from_orm(review)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{commit_id}/review", response_model=CommitReviewResponse)
async def update_commit_review(
    commit_id: int,
    review_data: CommitReviewUpdateRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Update commit review status"""
    factory = RepositoryFactory(db)
    review_service = CommitReviewService(factory.get_commit_review_repository())
    
    try:
        review = await review_service.update_review_status(
            commit_id=commit_id,
            reviewer_id=review_data.reviewer_id,
            status=review_data.status
        )
        return CommitReviewResponse.from_orm(review)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/pending-reviews/{reviewer_id}", response_model=List[CommitResponse])
async def get_pending_reviews(
    reviewer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get commits pending review by user"""
    factory = RepositoryFactory(db)
    commit_service = CommitService(factory.get_commit_repository())
    
    commits = await commit_service.get_pending_reviews(reviewer_id)
    return [CommitResponse.from_orm(commit) for commit in commits]
```

### Error Handling

#### Global Exception Handler
Location: `src/haven/interface/api/exceptions/ttr_exceptions.py`

```python
from fastapi import HTTPException, status
from haven.domain.exceptions.repository_exceptions import (
    EntityNotFoundException, DuplicateEntityException, ValidationException
)

def handle_repository_exceptions(func):
    """Decorator to handle repository exceptions"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except EntityNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except DuplicateEntityException as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except ValidationException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    return wrapper
```

### Route Registration
Location: `src/haven/interface/api/routes/ttr/__init__.py`

```python
from fastapi import APIRouter
from .users import router as users_router
from .repositories import router as repositories_router
from .commits import router as commits_router
from .comments import router as comments_router

ttr_router = APIRouter(prefix="/api/v1/ttr", tags=["ttr"])

ttr_router.include_router(users_router)
ttr_router.include_router(repositories_router)
ttr_router.include_router(commits_router)
ttr_router.include_router(comments_router)
```

### Integration with Main App
Update `src/haven/interface/api/main.py`:

```python
from fastapi import FastAPI
from haven.interface.api.routes.ttr import ttr_router

app = FastAPI(title="Haven API", version="1.0.0")

# Include TTR routes
app.include_router(ttr_router)
```

## Testing

### API Tests
Location: `tests/integration/api/ttr/test_user_endpoints.py`

```python
import pytest
from httpx import AsyncClient
from haven.interface.api.main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/ttr/users/", json={
            "username": "testuser",
            "email": "test@example.com",
            "display_name": "Test User"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/ttr/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
```

## Authentication (Future Enhancement)

### JWT Token Authentication
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

## Definition of Done
- [ ] All REST API endpoints implemented
- [ ] Request/response models with validation
- [ ] Proper error handling and HTTP status codes
- [ ] API documentation with OpenAPI/Swagger
- [ ] Unit tests for all endpoints
- [ ] Integration tests with database
- [ ] Authentication/authorization implemented
- [ ] Performance considerations addressed
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added