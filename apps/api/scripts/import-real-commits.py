#!/usr/bin/env python
"""Import real commits from the current repository."""

import asyncio
import subprocess
from datetime import datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from haven.domain.entities.commit import Commit, DiffStats
from haven.infrastructure.database.repositories.commit_repository import SQLAlchemyCommitRepository
from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl
from haven.domain.entities.repository import Repository


def get_commit_info(commit_hash: str) -> dict:
    """Get commit information using git."""
    # Get commit details
    format_string = "%H%n%s%n%an%n%ae%n%cn%n%ce%n%aI"
    result = subprocess.run(
        ["git", "show", "-s", f"--format={format_string}", commit_hash],
        capture_output=True,
        text=True,
        check=True
    )
    
    lines = result.stdout.strip().split('\n')
    
    # Get diff stats
    stats_result = subprocess.run(
        ["git", "show", "--stat", "--format=", commit_hash],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Parse diff stats from the last line
    stats_lines = stats_result.stdout.strip().split('\n')
    if stats_lines:
        last_line = stats_lines[-1]
        # Example: "10 files changed, 505 insertions(+), 2 deletions(-)"
        files_changed = 0
        insertions = 0
        deletions = 0
        
        parts = last_line.split(',')
        for part in parts:
            part = part.strip()
            if 'file' in part:
                files_changed = int(part.split()[0])
            elif 'insertion' in part:
                insertions = int(part.split()[0])
            elif 'deletion' in part:
                deletions = int(part.split()[0])
    else:
        files_changed = insertions = deletions = 0
    
    return {
        'hash': lines[0],
        'message': lines[1],
        'author_name': lines[2],
        'author_email': lines[3],
        'committer_name': lines[4],
        'committer_email': lines[5],
        'committed_at': datetime.fromisoformat(lines[6].replace('Z', '+00:00')),
        'diff_stats': {
            'files_changed': files_changed,
            'insertions': insertions,
            'deletions': deletions,
        }
    }


async def import_commits(commit_hashes: list[str]):
    """Import the specified commits into the database."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=True
    )
    
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        repo_repository = RepositoryRepositoryImpl(session)
        commit_repository = SQLAlchemyCommitRepository(session)
        
        # Get the current repository path
        repo_path = Path.cwd()
        repo_name = repo_path.name
        
        # First, create a repository if it doesn't exist
        existing_repo = await repo_repository.get_by_id(1)
        if not existing_repo:
            repo = Repository(
                name=repo_name,
                full_name=f"local/{repo_name}",
                url=str(repo_path),
                branch="main",
                description=f"Local repository: {repo_name}",
                is_local=True,
            )
            repo = await repo_repository.create(repo)
            await session.commit()
            print(f"Created repository: {repo.name} (ID: {repo.id})")
        else:
            repo = existing_repo
            print(f"Using existing repository: {repo.name} (ID: {repo.id})")
        
        # Import each commit
        for i, commit_hash in enumerate(commit_hashes):
            try:
                # Get commit info from git
                info = get_commit_info(commit_hash)
                
                # Create commit entity
                commit = Commit(
                    repository_id=repo.id,
                    commit_hash=info['hash'],
                    message=info['message'],
                    author_name=info['author_name'],
                    author_email=info['author_email'],
                    committer_name=info['committer_name'],
                    committer_email=info['committer_email'],
                    committed_at=info['committed_at'],
                    diff_stats=DiffStats(
                        files_changed=info['diff_stats']['files_changed'],
                        insertions=info['diff_stats']['insertions'],
                        deletions=info['diff_stats']['deletions'],
                    ),
                )
                
                # Check if commit already exists
                existing = await commit_repository.get_by_hash(repo.id, info['hash'])
                if not existing:
                    saved_commit = await commit_repository.create(commit)
                    print(f"Imported commit {i+1}/{len(commit_hashes)}: {saved_commit.short_hash} - {info['message'][:50]}")
                else:
                    print(f"Commit already exists: {info['hash'][:7]} - {info['message'][:50]}")
                
            except Exception as e:
                print(f"Error importing commit {commit_hash}: {e}")
        
        await session.commit()
        print(f"\nDone! Imported {len(commit_hashes)} commits for repository ID: {repo.id}")
        print(f"View them at: http://web.haven.local/repository/{repo.id}/browse")


async def main():
    """Main function."""
    # Get the last 3 commits
    commit_hashes = [
        "e6111cc",  # docs: Update work log with repository browser implementation
        "5bd9b2e",  # feat: Add repository browser with paginated commit list
        "fb6d76c",  # docs: Update roadmap and work log with diff viewer completion
    ]
    
    print(f"Importing {len(commit_hashes)} commits from the current repository...")
    await import_commits(commit_hashes)


if __name__ == "__main__":
    asyncio.run(main())