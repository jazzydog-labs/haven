"""API routes for repository management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from haven.infrastructure.database.dependencies import get_db
from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl
from haven.infrastructure.git.git_client import GitClient

router = APIRouter(prefix="/api/v1/repositories", tags=["repositories"])


class RepositoryResponse(BaseModel):
    """Response model for repository."""
    id: int
    repository_hash: str | None
    slug: str | None
    name: str
    full_name: str
    url: str  # Local path
    remote_url: str | None
    branch: str
    description: str | None
    is_local: bool
    created_at: datetime
    updated_at: datetime


class RepositoryWithStatsResponse(RepositoryResponse):
    """Repository response with additional statistics."""
    commit_count: int = 0
    branch_count: int = 0
    current_branch: str | None = None


@router.get("/{repository_identifier}", response_model=RepositoryWithStatsResponse)
async def get_repository_by_identifier(
    repository_identifier: str,
    db: AsyncSession = Depends(get_db),
) -> RepositoryWithStatsResponse:
    """Get repository by hash or slug with statistics."""
    repo_impl = RepositoryRepositoryImpl(db)
    
    # Try to get by slug first, then by hash
    repository = await repo_impl.get_by_slug(repository_identifier)
    if not repository:
        repository = await repo_impl.get_by_hash(repository_identifier)
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Get additional info from git
    git_client = GitClient()
    try:
        # Get remote URL
        remote_url = await git_client.get_remote_url(repository.url)
        if remote_url and not repository.remote_url:
            repository.remote_url = remote_url
            await repo_impl.update(repository)
        
        # Get branch info
        current_branch = await git_client.get_current_branch(repository.url)
        branches = await git_client.get_branches(repository.url)
        
        # Get commit count
        commit_count = await git_client.get_commit_count(repository.url, repository.branch)
    except Exception:
        # If git operations fail, return defaults
        current_branch = repository.branch
        branches = []
        commit_count = 0
    
    return RepositoryWithStatsResponse(
        id=repository.id,
        repository_hash=repository.repository_hash,
        slug=repository.slug,
        name=repository.name,
        full_name=repository.full_name,
        url=repository.url,
        remote_url=repository.remote_url,
        branch=repository.branch,
        description=repository.description,
        is_local=repository.is_local,
        created_at=repository.created_at,
        updated_at=repository.updated_at,
        commit_count=commit_count,
        branch_count=len(branches),
        current_branch=current_branch,
    )


@router.get("/", response_model=list[RepositoryResponse])
async def list_repositories(
    db: AsyncSession = Depends(get_db),
) -> list[RepositoryResponse]:
    """List all repositories."""
    repo_impl = RepositoryRepositoryImpl(db)
    repositories = await repo_impl.get_all()
    
    return [
        RepositoryResponse(
            id=repo.id,
            repository_hash=repo.repository_hash,
            slug=repo.slug,
            name=repo.name,
            full_name=repo.full_name,
            url=repo.url,
            remote_url=repo.remote_url,
            branch=repo.branch,
            description=repo.description,
            is_local=repo.is_local,
            created_at=repo.created_at,
            updated_at=repo.updated_at,
        )
        for repo in repositories
    ]