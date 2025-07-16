# Create TTR GraphQL Schema

## Description
Create GraphQL schema and resolvers for the TTR system using Strawberry GraphQL, providing a flexible query interface for the frontend.

## Acceptance Criteria
- [ ] GraphQL schema for all TTR entities
- [ ] Query and mutation resolvers
- [ ] Proper error handling and validation
- [ ] Subscription support for real-time updates
- [ ] Integration with existing Strawberry patterns
- [ ] GraphQL playground/GraphiQL integration

## Implementation Details

### GraphQL Schema Structure
```
src/haven/interface/graphql/ttr/
├── __init__.py
├── types/
│   ├── __init__.py
│   ├── user.py           # User types
│   ├── repository.py     # Repository types
│   ├── commit.py         # Commit types
│   └── comment.py        # Comment types
├── resolvers/
│   ├── __init__.py
│   ├── user_resolver.py
│   ├── repository_resolver.py
│   ├── commit_resolver.py
│   └── comment_resolver.py
├── queries.py            # Query root
├── mutations.py          # Mutation root
└── subscriptions.py      # Subscription root
```

### GraphQL Types

#### User Types
Location: `src/haven/interface/graphql/ttr/types/user.py`

```python
import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class User:
    id: int
    username: str
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

@strawberry.input
class UserCreateInput:
    username: str
    email: str
    display_name: str
    avatar_url: Optional[str] = None

@strawberry.input
class UserUpdateInput:
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None

@strawberry.type
class UserConnection:
    nodes: List[User]
    total_count: int
```

#### Repository Types
Location: `src/haven/interface/graphql/ttr/types/repository.py`

```python
import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class Repository:
    id: int
    name: str
    full_name: str
    url: str
    branch: str
    description: Optional[str] = None
    is_local: bool
    created_at: datetime
    updated_at: datetime

@strawberry.input
class RepositoryCreateInput:
    name: str
    full_name: str
    url: str
    branch: str = "main"
    description: Optional[str] = None
    is_local: bool = True

@strawberry.input
class RepositoryUpdateInput:
    name: Optional[str] = None
    full_name: Optional[str] = None
    branch: Optional[str] = None
    description: Optional[str] = None

@strawberry.type
class RepositoryConnection:
    nodes: List[Repository]
    total_count: int

@strawberry.type
class SyncResult:
    success: bool
    commits_added: int
    commits_updated: int
    message: str
```

#### Commit Types
Location: `src/haven/interface/graphql/ttr/types/commit.py`

```python
import strawberry
from typing import Optional, List
from datetime import datetime
from enum import Enum

@strawberry.enum
class ReviewStatus(Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    DRAFT = "draft"

@strawberry.type
class DiffStats:
    files_changed: int
    insertions: int
    deletions: int
    total_changes: int

@strawberry.type
class Commit:
    id: int
    repository_id: int
    commit_hash: str
    message: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    committed_at: datetime
    diff_stats: DiffStats
    short_hash: str
    short_message: str
    created_at: datetime
    updated_at: datetime

@strawberry.type
class CommitReview:
    id: int
    commit_id: int
    reviewer_id: int
    status: ReviewStatus
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

@strawberry.input
class CommitFilterInput:
    repository_id: Optional[int] = None
    status: Optional[ReviewStatus] = None
    author_email: Optional[str] = None

@strawberry.input
class ReviewUpdateInput:
    commit_id: int
    reviewer_id: int
    status: ReviewStatus

@strawberry.type
class CommitConnection:
    nodes: List[Commit]
    total_count: int
    page_info: PageInfo

@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str] = None
    end_cursor: Optional[str] = None
```

#### Comment Types
Location: `src/haven/interface/graphql/ttr/types/comment.py`

```python
import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class Comment:
    id: int
    commit_id: int
    user_id: int
    content: str
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_line_specific: bool
    preview: str

@strawberry.input
class CommentCreateInput:
    commit_id: int
    user_id: int
    content: str
    line_number: Optional[int] = None
    file_path: Optional[str] = None

@strawberry.input
class CommentUpdateInput:
    content: str

@strawberry.type
class CommentConnection:
    nodes: List[Comment]
    total_count: int
```

### GraphQL Resolvers

#### User Resolver
Location: `src/haven/interface/graphql/ttr/resolvers/user_resolver.py`

```python
import strawberry
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from haven.interface.graphql.ttr.types.user import User, UserCreateInput, UserUpdateInput
from haven.application.services.user_service import UserService
from haven.infrastructure.database.repositories.factory import RepositoryFactory

@strawberry.type
class UserResolver:
    @strawberry.field
    async def users(self, info) -> List[User]:
        """Get all users"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        user_service = UserService(factory.get_user_repository())
        
        users = await user_service.get_all_users()
        return [self._to_graphql_user(user) for user in users]
    
    @strawberry.field
    async def user(self, info, id: int) -> Optional[User]:
        """Get user by ID"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        user_service = UserService(factory.get_user_repository())
        
        user = await user_service.get_user_by_id(id)
        return self._to_graphql_user(user) if user else None
    
    @strawberry.field
    async def user_by_username(self, info, username: str) -> Optional[User]:
        """Get user by username"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        user_service = UserService(factory.get_user_repository())
        
        user = await user_service.get_user_by_username(username)
        return self._to_graphql_user(user) if user else None
    
    @strawberry.mutation
    async def create_user(self, info, input: UserCreateInput) -> User:
        """Create a new user"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        user_service = UserService(factory.get_user_repository())
        
        user = await user_service.create_user(
            username=input.username,
            email=input.email,
            display_name=input.display_name,
            avatar_url=input.avatar_url
        )
        return self._to_graphql_user(user)
    
    @strawberry.mutation
    async def update_user(self, info, id: int, input: UserUpdateInput) -> User:
        """Update user"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        user_service = UserService(factory.get_user_repository())
        
        user = await user_service.update_user(
            user_id=id,
            display_name=input.display_name,
            avatar_url=input.avatar_url
        )
        return self._to_graphql_user(user)
    
    @strawberry.mutation
    async def delete_user(self, info, id: int) -> bool:
        """Delete user"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        user_service = UserService(factory.get_user_repository())
        
        return await user_service.delete_user(id)
    
    def _to_graphql_user(self, user) -> User:
        """Convert domain entity to GraphQL type"""
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
```

#### Repository Resolver
Location: `src/haven/interface/graphql/ttr/resolvers/repository_resolver.py`

```python
import strawberry
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from haven.interface.graphql.ttr.types.repository import (
    Repository, RepositoryCreateInput, RepositoryUpdateInput, SyncResult
)
from haven.application.services.repository_service import RepositoryService
from haven.infrastructure.database.repositories.factory import RepositoryFactory

@strawberry.type
class RepositoryResolver:
    @strawberry.field
    async def repositories(self, info) -> List[Repository]:
        """Get all repositories"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        repo_service = RepositoryService(factory.get_repository_repository())
        
        repositories = await repo_service.get_all_repositories()
        return [self._to_graphql_repository(repo) for repo in repositories]
    
    @strawberry.field
    async def repository(self, info, id: int) -> Optional[Repository]:
        """Get repository by ID"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        repo_service = RepositoryService(factory.get_repository_repository())
        
        repository = await repo_service.get_repository_by_id(id)
        return self._to_graphql_repository(repository) if repository else None
    
    @strawberry.mutation
    async def create_repository(self, info, input: RepositoryCreateInput) -> Repository:
        """Create a new repository"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        repo_service = RepositoryService(factory.get_repository_repository())
        
        repository = await repo_service.create_repository(
            name=input.name,
            full_name=input.full_name,
            url=input.url,
            branch=input.branch,
            description=input.description,
            is_local=input.is_local
        )
        return self._to_graphql_repository(repository)
    
    @strawberry.mutation
    async def sync_repository(self, info, id: int, force: bool = False) -> SyncResult:
        """Sync repository commits"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        repo_service = RepositoryService(factory.get_repository_repository())
        
        result = await repo_service.sync_repository_commits(id, force)
        return SyncResult(
            success=result["success"],
            commits_added=result["commits_added"],
            commits_updated=result["commits_updated"],
            message=result["message"]
        )
    
    def _to_graphql_repository(self, repo) -> Repository:
        """Convert domain entity to GraphQL type"""
        return Repository(
            id=repo.id,
            name=repo.name,
            full_name=repo.full_name,
            url=repo.url,
            branch=repo.branch,
            description=repo.description,
            is_local=repo.is_local,
            created_at=repo.created_at,
            updated_at=repo.updated_at
        )
```

#### Commit Resolver
Location: `src/haven/interface/graphql/ttr/resolvers/commit_resolver.py`

```python
import strawberry
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from haven.interface.graphql.ttr.types.commit import (
    Commit, CommitReview, CommitFilterInput, ReviewUpdateInput, 
    CommitConnection, DiffStats, ReviewStatus
)
from haven.application.services.commit_service import CommitService
from haven.application.services.commit_review_service import CommitReviewService
from haven.infrastructure.database.repositories.factory import RepositoryFactory

@strawberry.type
class CommitResolver:
    @strawberry.field
    async def commits(
        self, 
        info, 
        first: int = 50,
        after: Optional[str] = None,
        filter: Optional[CommitFilterInput] = None
    ) -> CommitConnection:
        """Get commits with pagination and filtering"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        commit_service = CommitService(factory.get_commit_repository())
        
        commits = await commit_service.get_commits(
            repository_id=filter.repository_id if filter else None,
            status=filter.status if filter else None,
            limit=first,
            after=after
        )
        
        return CommitConnection(
            nodes=[self._to_graphql_commit(commit) for commit in commits],
            total_count=len(commits),
            page_info=PageInfo(
                has_next_page=len(commits) == first,
                has_previous_page=after is not None,
                start_cursor=str(commits[0].id) if commits else None,
                end_cursor=str(commits[-1].id) if commits else None
            )
        )
    
    @strawberry.field
    async def commit(self, info, id: int) -> Optional[Commit]:
        """Get commit by ID"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        commit_service = CommitService(factory.get_commit_repository())
        
        commit = await commit_service.get_commit_by_id(id)
        return self._to_graphql_commit(commit) if commit else None
    
    @strawberry.field
    async def commit_by_hash(self, info, repository_id: int, commit_hash: str) -> Optional[Commit]:
        """Get commit by hash"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        commit_service = CommitService(factory.get_commit_repository())
        
        commit = await commit_service.get_commit_by_hash(repository_id, commit_hash)
        return self._to_graphql_commit(commit) if commit else None
    
    @strawberry.field
    async def pending_reviews(self, info, reviewer_id: int) -> List[Commit]:
        """Get commits pending review by user"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        commit_service = CommitService(factory.get_commit_repository())
        
        commits = await commit_service.get_pending_reviews(reviewer_id)
        return [self._to_graphql_commit(commit) for commit in commits]
    
    @strawberry.field
    async def commit_diff(self, info, id: int) -> str:
        """Get commit diff"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        commit_service = CommitService(factory.get_commit_repository())
        
        return await commit_service.get_commit_diff(id)
    
    @strawberry.mutation
    async def update_review(self, info, input: ReviewUpdateInput) -> CommitReview:
        """Update commit review status"""
        session: AsyncSession = info.context["session"]
        factory = RepositoryFactory(session)
        review_service = CommitReviewService(factory.get_commit_review_repository())
        
        review = await review_service.update_review_status(
            commit_id=input.commit_id,
            reviewer_id=input.reviewer_id,
            status=input.status
        )
        return self._to_graphql_review(review)
    
    def _to_graphql_commit(self, commit) -> Commit:
        """Convert domain entity to GraphQL type"""
        return Commit(
            id=commit.id,
            repository_id=commit.repository_id,
            commit_hash=commit.commit_hash,
            message=commit.message,
            author_name=commit.author_name,
            author_email=commit.author_email,
            committer_name=commit.committer_name,
            committer_email=commit.committer_email,
            committed_at=commit.committed_at,
            diff_stats=DiffStats(
                files_changed=commit.diff_stats.files_changed,
                insertions=commit.diff_stats.insertions,
                deletions=commit.diff_stats.deletions,
                total_changes=commit.diff_stats.total_changes
            ),
            short_hash=commit.short_hash,
            short_message=commit.short_message,
            created_at=commit.created_at,
            updated_at=commit.updated_at
        )
    
    def _to_graphql_review(self, review) -> CommitReview:
        """Convert domain entity to GraphQL type"""
        return CommitReview(
            id=review.id,
            commit_id=review.commit_id,
            reviewer_id=review.reviewer_id,
            status=ReviewStatus(review.status.value),
            reviewed_at=review.reviewed_at,
            created_at=review.created_at,
            updated_at=review.updated_at
        )
```

### GraphQL Schema Root

#### Query Root
Location: `src/haven/interface/graphql/ttr/queries.py`

```python
import strawberry
from typing import List, Optional

from .resolvers.user_resolver import UserResolver
from .resolvers.repository_resolver import RepositoryResolver
from .resolvers.commit_resolver import CommitResolver
from .resolvers.comment_resolver import CommentResolver
from .types.user import User
from .types.repository import Repository
from .types.commit import Commit, CommitConnection, CommitFilterInput
from .types.comment import Comment

@strawberry.type
class TTRQuery:
    # User queries
    users: List[User] = strawberry.field(resolver=UserResolver().users)
    user: Optional[User] = strawberry.field(resolver=UserResolver().user)
    user_by_username: Optional[User] = strawberry.field(resolver=UserResolver().user_by_username)
    
    # Repository queries
    repositories: List[Repository] = strawberry.field(resolver=RepositoryResolver().repositories)
    repository: Optional[Repository] = strawberry.field(resolver=RepositoryResolver().repository)
    
    # Commit queries
    commits: CommitConnection = strawberry.field(resolver=CommitResolver().commits)
    commit: Optional[Commit] = strawberry.field(resolver=CommitResolver().commit)
    commit_by_hash: Optional[Commit] = strawberry.field(resolver=CommitResolver().commit_by_hash)
    pending_reviews: List[Commit] = strawberry.field(resolver=CommitResolver().pending_reviews)
    commit_diff: str = strawberry.field(resolver=CommitResolver().commit_diff)
    
    # Comment queries
    comments: List[Comment] = strawberry.field(resolver=CommentResolver().comments)
    commit_comments: List[Comment] = strawberry.field(resolver=CommentResolver().commit_comments)
    line_comments: List[Comment] = strawberry.field(resolver=CommentResolver().line_comments)
```

#### Mutation Root
Location: `src/haven/interface/graphql/ttr/mutations.py`

```python
import strawberry
from .resolvers.user_resolver import UserResolver
from .resolvers.repository_resolver import RepositoryResolver
from .resolvers.commit_resolver import CommitResolver
from .resolvers.comment_resolver import CommentResolver
from .types.user import User, UserCreateInput, UserUpdateInput
from .types.repository import Repository, RepositoryCreateInput, SyncResult
from .types.commit import CommitReview, ReviewUpdateInput
from .types.comment import Comment, CommentCreateInput, CommentUpdateInput

@strawberry.type
class TTRMutation:
    # User mutations
    create_user: User = strawberry.field(resolver=UserResolver().create_user)
    update_user: User = strawberry.field(resolver=UserResolver().update_user)
    delete_user: bool = strawberry.field(resolver=UserResolver().delete_user)
    
    # Repository mutations
    create_repository: Repository = strawberry.field(resolver=RepositoryResolver().create_repository)
    sync_repository: SyncResult = strawberry.field(resolver=RepositoryResolver().sync_repository)
    
    # Commit mutations
    update_review: CommitReview = strawberry.field(resolver=CommitResolver().update_review)
    
    # Comment mutations
    create_comment: Comment = strawberry.field(resolver=CommentResolver().create_comment)
    update_comment: Comment = strawberry.field(resolver=CommentResolver().update_comment)
    delete_comment: bool = strawberry.field(resolver=CommentResolver().delete_comment)
```

### Integration with Main Schema

Update `src/haven/interface/graphql/schema.py`:

```python
import strawberry
from .ttr.queries import TTRQuery
from .ttr.mutations import TTRMutation

@strawberry.type
class Query(TTRQuery):
    @strawberry.field
    def health(self) -> str:
        return "OK"

@strawberry.type
class Mutation(TTRMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

## Subscriptions (Real-time Updates)

### Subscription Types
Location: `src/haven/interface/graphql/ttr/subscriptions.py`

```python
import strawberry
from typing import AsyncGenerator
from .types.commit import Commit, CommitReview
from .types.comment import Comment

@strawberry.type
class TTRSubscription:
    @strawberry.subscription
    async def commit_reviews_updated(
        self, 
        info, 
        repository_id: int
    ) -> AsyncGenerator[CommitReview, None]:
        """Subscribe to commit review updates"""
        # Implementation depends on your pub/sub system
        pass
    
    @strawberry.subscription
    async def new_comments(
        self, 
        info, 
        commit_id: int
    ) -> AsyncGenerator[Comment, None]:
        """Subscribe to new comments on a commit"""
        # Implementation depends on your pub/sub system
        pass
```

## Testing

### GraphQL Tests
Location: `tests/integration/graphql/ttr/test_user_queries.py`

```python
import pytest
from strawberry.test import BaseGraphQLTestClient
from haven.interface.graphql.schema import schema

@pytest.fixture
def graphql_client():
    return BaseGraphQLTestClient(schema)

def test_users_query(graphql_client):
    query = """
    query {
        users {
            id
            username
            email
            displayName
        }
    }
    """
    
    result = graphql_client.query(query)
    assert result.errors is None
    assert "users" in result.data

def test_create_user_mutation(graphql_client):
    mutation = """
    mutation {
        createUser(input: {
            username: "testuser"
            email: "test@example.com"
            displayName: "Test User"
        }) {
            id
            username
            email
        }
    }
    """
    
    result = graphql_client.query(mutation)
    assert result.errors is None
    assert result.data["createUser"]["username"] == "testuser"
```

## Performance Considerations

### DataLoader Pattern
```python
from strawberry.dataloader import DataLoader
from typing import List

async def load_users(keys: List[int]) -> List[User]:
    """Batch load users by IDs"""
    # Implementation to batch load users
    pass

user_loader = DataLoader(load_fn=load_users)
```

### Query Complexity Analysis
```python
from strawberry.extensions import QueryDepthLimiter

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(max_depth=10)
    ]
)
```

## Definition of Done
- [ ] GraphQL schema implemented for all TTR entities
- [ ] Query and mutation resolvers created
- [ ] Proper error handling and validation
- [ ] GraphQL types with proper field resolvers
- [ ] Integration with existing Strawberry patterns
- [ ] Unit tests for all resolvers
- [ ] Integration tests for complex queries
- [ ] Performance optimizations (DataLoader, etc.)
- [ ] GraphQL playground integration
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Work log entry added