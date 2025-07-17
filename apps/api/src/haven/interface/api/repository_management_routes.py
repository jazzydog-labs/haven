"""API routes for repository management operations."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from haven.infrastructure.database.dependencies import get_db
from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl
from haven.infrastructure.database.repositories.commit_repository import SQLAlchemyCommitRepository
from haven.infrastructure.git.git_client import GitClient
from haven.domain.entities.commit import Commit, DiffStats
import hashlib

router = APIRouter(prefix="/api/v1/repository-management", tags=["repository-management"])


class LoadCommitsRequest(BaseModel):
    """Request to load commits from repository."""
    branch: str = "main"
    limit: Optional[int] = None  # None means load all commits
    since_date: Optional[datetime] = None  # Load commits since this date


class LoadCommitsResponse(BaseModel):
    """Response for load commits operation."""
    status: str
    message: str
    task_id: Optional[str] = None


async def _load_commits_task(
    repository_id: int,
    branch: str,
    limit: Optional[int],
    since_date: Optional[datetime],
    db_session: AsyncSession,
):
    """Background task to load commits from repository."""
    repo_impl = RepositoryRepositoryImpl(db_session)
    commit_repo = SQLAlchemyCommitRepository(db_session)
    
    # Get repository
    repository = await repo_impl.get_by_id(repository_id)
    if not repository:
        return
    
    # If no since_date specified, find latest commit date to avoid duplicates
    if not since_date:
        existing_commits = await commit_repo.get_by_repository(repository.id)
        if existing_commits:
            # Find the latest commit date
            latest_commit = max(existing_commits, key=lambda c: c.committed_at)
            since_date = latest_commit.committed_at
            print(f"Loading commits since: {since_date}")
    
    # Get commits from git
    git_client = GitClient()
    try:
        # Get commit log
        commits_data = await git_client.get_commit_log(
            repository.url,
            branch=branch,
            limit=limit,
            since_date=since_date
        )
        
        # Process each commit
        loaded_count = 0
        skipped_count = 0
        
        for commit_data in commits_data:
            # Check if commit already exists
            existing = await commit_repo.get_by_hash(repository.id, commit_data["hash"])
            if existing:
                skipped_count += 1
                continue
            
            # Create commit entity
            commit = Commit(
                repository_id=repository.id,
                commit_hash=commit_data["hash"],
                message=commit_data["message"],
                author_name=commit_data["author_name"],
                author_email=commit_data["author_email"],
                committer_name=commit_data["committer_name"],
                committer_email=commit_data["committer_email"],
                committed_at=commit_data["committed_at"],
                diff_stats=DiffStats(
                    files_changed=commit_data.get("files_changed", 0),
                    insertions=commit_data.get("insertions", 0),
                    deletions=commit_data.get("deletions", 0),
                ),
            )
            
            # Save commit
            await commit_repo.create(commit)
            loaded_count += 1
        
        await db_session.commit()
        print(f"Loaded {loaded_count} new commits, skipped {skipped_count} existing commits for repository {repository.name}")
        
    except Exception as e:
        print(f"Error loading commits: {str(e)}")
        await db_session.rollback()


@router.post("/{repository_identifier}/load-commits", response_model=LoadCommitsResponse)
async def load_commits(
    repository_identifier: str,
    request: LoadCommitsRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> LoadCommitsResponse:
    """Load commits from repository into database."""
    repo_impl = RepositoryRepositoryImpl(db)
    
    # Try to get by slug first, then by hash
    repository = await repo_impl.get_by_slug(repository_identifier)
    if not repository:
        repository = await repo_impl.get_by_hash(repository_identifier)
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Generate task ID
    task_id = hashlib.sha256(f"{repository.id}-{datetime.utcnow()}".encode()).hexdigest()[:16]
    
    # Start background task
    background_tasks.add_task(
        _load_commits_task,
        repository.id,
        request.branch,
        request.limit,
        request.since_date,
        db,
    )
    
    return LoadCommitsResponse(
        status="started",
        message=f"Started loading commits from branch '{request.branch}'",
        task_id=task_id,
    )


class RepositoryStatsResponse(BaseModel):
    """Repository statistics."""
    total_commits: int
    total_branches: int
    latest_commit_date: Optional[datetime]
    oldest_commit_date: Optional[datetime]


@router.get("/{repository_identifier}/stats", response_model=RepositoryStatsResponse)
async def get_repository_stats(
    repository_identifier: str,
    db: AsyncSession = Depends(get_db),
) -> RepositoryStatsResponse:
    """Get repository statistics."""
    repo_impl = RepositoryRepositoryImpl(db)
    commit_repo = SQLAlchemyCommitRepository(db)
    
    # Try to get by slug first, then by hash
    repository = await repo_impl.get_by_slug(repository_identifier)
    if not repository:
        repository = await repo_impl.get_by_hash(repository_identifier)
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Get commit count
    commits = await commit_repo.get_by_repository(repository.id)
    total_commits = len(commits)
    
    # Get date range
    latest_commit_date = None
    oldest_commit_date = None
    if commits:
        sorted_commits = sorted(commits, key=lambda c: c.committed_at)
        oldest_commit_date = sorted_commits[0].committed_at
        latest_commit_date = sorted_commits[-1].committed_at
    
    # Get branch count from git
    git_client = GitClient()
    try:
        branches = await git_client.get_branches(repository.url)
        total_branches = len(branches)
    except:
        total_branches = 1  # At least main/master
    
    return RepositoryStatsResponse(
        total_commits=total_commits,
        total_branches=total_branches,
        latest_commit_date=latest_commit_date,
        oldest_commit_date=oldest_commit_date,
    )