"""API routes for commit management and diff generation."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from haven.application.services.diff_html_service import DiffHtmlService
from haven.domain.entities.commit import Commit, CommitReview
from haven.infrastructure.database.dependencies import get_db
from haven.infrastructure.database.repositories.commit_repository import (
    SQLAlchemyCommitRepository,
    SQLAlchemyCommitReviewRepository,
)
from haven.infrastructure.git.git_client import GitClient
from haven.interface.api.schemas.commit_schemas import (
    CommitCreate,
    CommitDiffResponse,
    CommitResponse,
    CommitWithReviewResponse,
    CommitReviewCreate,
    CommitReviewResponse,
    PaginatedCommitResponse,
    PaginatedCommitWithReviewResponse,
    ReviewCommentCreate,
    ReviewCommentResponse,
)
from haven.domain.entities.commit import ReviewStatus
from sqlalchemy import func, desc

router = APIRouter(prefix="/api/v1/commits", tags=["commits"])


@router.post("/", response_model=CommitResponse)
async def create_commit(
    commit_data: CommitCreate,
    db: AsyncSession = Depends(get_db),
) -> CommitResponse:
    """Create a new commit record."""
    repo = SQLAlchemyCommitRepository(db)

    # Create commit entity
    commit = Commit(
        repository_id=commit_data.repository_id,
        commit_hash=commit_data.commit_hash,
        message=commit_data.message,
        author_name=commit_data.author_name,
        author_email=commit_data.author_email,
        committer_name=commit_data.committer_name,
        committer_email=commit_data.committer_email,
        committed_at=commit_data.committed_at,
        diff_stats=commit_data.diff_stats,
    )

    # Save to database
    saved_commit = await repo.create(commit)
    await db.commit()

    return CommitResponse.from_entity(saved_commit)


@router.get("/", response_model=list[CommitResponse])
async def list_commits(
    repository_id: int = Query(..., description="Repository ID"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[CommitResponse]:
    """List commits for a repository."""
    repo = SQLAlchemyCommitRepository(db)
    commits = await repo.get_by_repository(repository_id, limit, offset)

    return [CommitResponse.from_entity(commit) for commit in commits]


@router.get("/paginated-with-reviews", response_model=PaginatedCommitWithReviewResponse)
async def list_commits_paginated_with_reviews(
    repository_id: int = Query(..., description="Repository ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=500, description="Items per page"),
    search: str | None = Query(None, description="Search in commit message or hash"),
    author: str | None = Query(None, description="Filter by author name or email"),
    date_from: str | None = Query(None, description="Filter commits from this date (ISO format)"),
    date_to: str | None = Query(None, description="Filter commits until this date (ISO format)"),
    branch: str | None = Query(None, description="Filter by branch name"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedCommitWithReviewResponse:
    """List commits with review status for a repository."""
    repo = SQLAlchemyCommitRepository(db)
    review_repo = SQLAlchemyCommitReviewRepository(db)

    # Calculate offset from page number
    offset = (page - 1) * page_size

    # Check if we have any search/filter parameters
    has_filters = any([search, author, date_from, date_to])

    if has_filters:
        # Use search method
        commits = await repo.search_commits(
            repository_id=repository_id,
            search_query=search,
            author_filter=author,
            date_from=date_from,
            date_to=date_to,
            limit=page_size,
            offset=offset,
        )
        total = await repo.count_search_results(
            repository_id=repository_id,
            search_query=search,
            author_filter=author,
            date_from=date_from,
            date_to=date_to,
        )
    else:
        # Use regular listing
        commits = await repo.get_by_repository(repository_id, page_size, offset)
        total = await repo.count_by_repository(repository_id)

    # Get reviews for all commits
    commit_ids = [c.id for c in commits]
    from haven.infrastructure.database.models import CommitReviewModel
    
    if commit_ids:
        # Get latest review status for each commit
        subquery = (
            select(
                CommitReviewModel.commit_id,
                func.max(CommitReviewModel.created_at).label("latest_created_at")
            )
            .filter(CommitReviewModel.commit_id.in_(commit_ids))
            .group_by(CommitReviewModel.commit_id)
            .subquery()
        )
        
        reviews_stmt = (
            select(
                CommitReviewModel.commit_id,
                CommitReviewModel.status,
                func.count(CommitReviewModel.id).label("review_count"),
                func.max(CommitReviewModel.reviewed_at).label("latest_review_at")
            )
            .join(
                subquery,
                (CommitReviewModel.commit_id == subquery.c.commit_id) &
                (CommitReviewModel.created_at == subquery.c.latest_created_at)
            )
            .group_by(CommitReviewModel.commit_id, CommitReviewModel.status)
        )
        
        reviews_query = await db.execute(reviews_stmt)
        
        review_map = {
            row.commit_id: {
                "status": ReviewStatus(row.status),
                "count": row.review_count,
                "latest_at": row.latest_review_at
            }
            for row in reviews_query
        }
    else:
        review_map = {}

    # Build response with reviews
    items_with_reviews = []
    for commit in commits:
        commit_response = CommitResponse.from_entity(commit)
        review_info = review_map.get(commit.id, {})
        
        items_with_reviews.append(
            CommitWithReviewResponse(
                **commit_response.model_dump(),
                review_status=review_info.get("status"),
                review_count=review_info.get("count", 0),
                latest_review_at=review_info.get("latest_at")
            )
        )

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return PaginatedCommitWithReviewResponse(
        items=items_with_reviews,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/paginated", response_model=PaginatedCommitResponse)
async def list_commits_paginated(
    repository_id: int = Query(..., description="Repository ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=500, description="Items per page"),
    search: str | None = Query(None, description="Search in commit message or hash"),
    author: str | None = Query(None, description="Filter by author name or email"),
    date_from: str | None = Query(None, description="Filter commits from this date (ISO format)"),
    date_to: str | None = Query(None, description="Filter commits until this date (ISO format)"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedCommitResponse:
    """List commits for a repository with pagination metadata and search/filter support."""
    repo = SQLAlchemyCommitRepository(db)

    # Calculate offset from page number
    offset = (page - 1) * page_size

    # Check if we have any search/filter parameters
    has_filters = any([search, author, date_from, date_to])

    if has_filters:
        # Use search method
        commits = await repo.search_commits(
            repository_id=repository_id,
            search_query=search,
            author_filter=author,
            date_from=date_from,
            date_to=date_to,
            limit=page_size,
            offset=offset,
        )
        total = await repo.count_search_results(
            repository_id=repository_id,
            search_query=search,
            author_filter=author,
            date_from=date_from,
            date_to=date_to,
        )
    else:
        # Use regular listing
        commits = await repo.get_by_repository(repository_id, page_size, offset)
        total = await repo.count_by_repository(repository_id)

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return PaginatedCommitResponse(
        items=[CommitResponse.from_entity(commit) for commit in commits],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/by-hash/{commit_hash}", response_model=CommitResponse)
async def get_commit_by_hash(
    commit_hash: str,
    repository_id: int = Query(..., description="Repository ID"),
    db: AsyncSession = Depends(get_db),
) -> CommitResponse:
    """Get a commit by hash."""
    repo = SQLAlchemyCommitRepository(db)
    commit = await repo.get_by_hash(repository_id, commit_hash)

    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")

    return CommitResponse.from_entity(commit)


@router.get("/hash/{commit_hash}", response_model=CommitResponse)
async def get_commit_by_hash_global(
    commit_hash: str,
    db: AsyncSession = Depends(get_db),
) -> CommitResponse:
    """Get a commit by hash across all repositories."""
    repo = SQLAlchemyCommitRepository(db)
    
    # Try to find commit by hash across all repositories
    from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl
    repo_impl = RepositoryRepositoryImpl(db)
    repositories = await repo_impl.get_all()
    
    for repository in repositories:
        commit = await repo.get_by_hash(repository.id, commit_hash)
        if commit:
            return CommitResponse.from_entity(commit)
    
    raise HTTPException(status_code=404, detail="Commit not found")


@router.get("/{commit_id}", response_model=CommitResponse)
async def get_commit(
    commit_id: int,
    db: AsyncSession = Depends(get_db),
) -> CommitResponse:
    """Get a commit by ID."""
    repo = SQLAlchemyCommitRepository(db)
    commit = await repo.get_by_id(commit_id)

    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")

    return CommitResponse.from_entity(commit)


@router.post("/{commit_id}/generate-diff", response_model=CommitDiffResponse)
async def generate_commit_diff(
    commit_id: int,
    db: AsyncSession = Depends(get_db),
) -> CommitDiffResponse:
    """Generate HTML diff for a commit."""
    repo = SQLAlchemyCommitRepository(db)
    commit = await repo.get_by_id(commit_id)

    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")

    # Initialize services
    git_client = GitClient()
    diff_service = DiffHtmlService(git_client, repo)

    # Get repository information
    from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl
    repo_impl = RepositoryRepositoryImpl(db)
    repository = await repo_impl.get_by_id(commit.repository_id)
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Generate diff HTML
    html_path = await diff_service.generate_diff_html(commit, repository.url)

    # Commit changes
    await db.commit()

    # Get updated commit
    updated_commit = await repo.get_by_id(commit_id)

    return CommitDiffResponse(
        commit_id=commit_id,
        diff_html_path=html_path,
        diff_generated_at=updated_commit.diff_generated_at,
    )


@router.post("/batch/generate-diffs")
async def generate_batch_diffs(
    commit_ids: list[int],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Generate HTML diffs for multiple commits in parallel."""
    repo = SQLAlchemyCommitRepository(db)

    # Get all commits
    commits = []
    for commit_id in commit_ids:
        commit = await repo.get_by_id(commit_id)
        if commit:
            commits.append(commit)

    if not commits:
        raise HTTPException(status_code=404, detail="No valid commits found")

    # Initialize services
    git_client = GitClient()
    diff_service = DiffHtmlService(git_client, repo)

    # Get repository information from first commit
    from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl
    repo_impl = RepositoryRepositoryImpl(db)
    repository = await repo_impl.get_by_id(commits[0].repository_id)
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Process commits in parallel
    results = await diff_service.process_commits_batch(commits, repository.url, max_concurrent=5)

    # Commit changes
    await db.commit()

    return {
        "processed": len(results),
        "results": results,
    }


@router.get("/{commit_id}/diff-html")
async def get_commit_diff_html(
    commit_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the HTML diff file for a commit (legacy)."""
    repo = SQLAlchemyCommitRepository(db)
    commit = await repo.get_by_id(commit_id)

    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")

    if not commit.diff_html_path:
        raise HTTPException(status_code=404, detail="Diff HTML not generated for this commit")

    # Check if file exists
    file_path = Path(commit.diff_html_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Diff HTML file not found")

    return FileResponse(
        path=str(file_path),
        media_type="text/html",
        filename=f"commit_{commit.short_hash}_diff.html",
    )


@router.get("/{commit_id}/diff-json")
async def get_commit_diff_json(
    commit_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the JSON diff data for a commit."""
    repo = SQLAlchemyCommitRepository(db)
    commit = await repo.get_by_id(commit_id)

    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")

    if not commit.diff_html_path:
        raise HTTPException(status_code=404, detail="Diff not generated for this commit")

    # Check if JSON file exists
    file_path = Path(commit.diff_html_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Diff file not found")

    # Read and return JSON content
    import json
    with open(file_path, 'r') as f:
        diff_data = json.load(f)
    
    return diff_data


# Review endpoints
@router.post("/{commit_id}/reviews", response_model=CommitReviewResponse)
async def create_commit_review(
    commit_id: int,
    review_data: CommitReviewCreate,
    db: AsyncSession = Depends(get_db),
) -> CommitReviewResponse:
    """Create a review for a commit."""
    # Check if commit exists
    commit_repo = SQLAlchemyCommitRepository(db)
    commit = await commit_repo.get_by_id(commit_id)

    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")

    # Create review
    review_repo = SQLAlchemyCommitReviewRepository(db)
    review = CommitReview(
        commit_id=commit_id,
        reviewer_id=review_data.reviewer_id,
        status=review_data.status,
        notes=review_data.notes,
    )

    saved_review = await review_repo.create(review)
    await db.commit()

    return CommitReviewResponse.from_entity(saved_review)


@router.get("/{commit_id}/reviews", response_model=list[CommitReviewResponse])
async def list_commit_reviews(
    commit_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[CommitReviewResponse]:
    """List all reviews for a commit."""
    review_repo = SQLAlchemyCommitReviewRepository(db)
    reviews = await review_repo.get_by_commit(commit_id)

    return [CommitReviewResponse.from_entity(review) for review in reviews]


# Review comment endpoints
@router.post("/{commit_id}/comments", response_model=ReviewCommentResponse)
async def create_review_comment(
    commit_id: int,
    comment_data: ReviewCommentCreate,
    db: AsyncSession = Depends(get_db),
) -> ReviewCommentResponse:
    """Create an inline comment on a commit."""
    # Check if commit exists
    commit_repo = SQLAlchemyCommitRepository(db)
    commit = await commit_repo.get_by_id(commit_id)
    
    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")
    
    # Import ReviewComment entity and repository
    from haven.domain.entities.review_comment import ReviewComment
    from haven.infrastructure.database.repositories.review_repository import SqlAlchemyReviewCommentRepository
    
    # Create review comment
    comment_repo = SqlAlchemyReviewCommentRepository(db)
    comment = ReviewComment(
        commit_id=commit_id,
        reviewer_id=comment_data.reviewer_id,
        line_number=comment_data.line_number,
        file_path=comment_data.file_path,
        content=comment_data.content,
    )
    
    saved_comment = await comment_repo.create(comment)
    await db.commit()
    
    return ReviewCommentResponse(
        id=saved_comment.id,
        commit_id=saved_comment.commit_id,
        reviewer_id=saved_comment.reviewer_id,
        line_number=saved_comment.line_number,
        file_path=saved_comment.file_path,
        content=saved_comment.content,
        created_at=saved_comment.created_at,
        updated_at=saved_comment.updated_at,
    )


@router.get("/{commit_id}/comments", response_model=list[ReviewCommentResponse])
async def list_review_comments(
    commit_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[ReviewCommentResponse]:
    """List all inline comments for a commit."""
    from haven.infrastructure.database.repositories.review_repository import SqlAlchemyReviewCommentRepository
    
    comment_repo = SqlAlchemyReviewCommentRepository(db)
    comments = await comment_repo.get_by_commit_id(commit_id)
    
    return [
        ReviewCommentResponse(
            id=comment.id,
            commit_id=comment.commit_id,
            reviewer_id=comment.reviewer_id,
            line_number=comment.line_number,
            file_path=comment.file_path,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
        for comment in comments
    ]
