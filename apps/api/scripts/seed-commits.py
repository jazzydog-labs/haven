#!/usr/bin/env python
"""Seed script to create sample commits for testing the repository browser."""

import asyncio
import random
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from haven.domain.entities.commit import Commit, DiffStats
from haven.domain.entities.repository import Repository
from haven.infrastructure.database.repositories.commit_repository import SQLAlchemyCommitRepository
from haven.infrastructure.database.repositories.repository_repository import (
    SQLAlchemyRepositoryRepository,
)


async def create_sample_commits():
    """Create sample commits for testing."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=True
    )

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        repo_repository = SQLAlchemyRepositoryRepository(session)
        commit_repository = SQLAlchemyCommitRepository(session)

        # First, create a repository if it doesn't exist
        existing_repo = await repo_repository.get_by_id(1)
        if not existing_repo:
            repo = Repository(
                name="haven",
                clone_url="https://github.com/example/haven.git",
                default_branch="main",
                description="Sample repository for testing",
                is_active=True,
            )
            repo = await repo_repository.create(repo)
            await session.commit()
            print(f"Created repository: {repo.name} (ID: {repo.id})")
        else:
            repo = existing_repo
            print(f"Using existing repository: {repo.name} (ID: {repo.id})")

        # Create sample commits
        commit_messages = [
            "Initial commit",
            "Add user authentication module",
            "Fix security vulnerability in auth",
            "Implement password reset functionality",
            "Add unit tests for auth module",
            "Refactor database connection handling",
            "Update dependencies to latest versions",
            "Add API documentation",
            "Implement rate limiting",
            "Fix memory leak in connection pool",
            "Add GraphQL support",
            "Improve error handling",
            "Add logging infrastructure",
            "Implement caching layer",
            "Add performance monitoring",
            "Fix race condition in async handler",
            "Update README with setup instructions",
            "Add CI/CD pipeline configuration",
            "Implement webhook support",
            "Add integration tests",
            "Refactor service layer",
            "Add database migrations",
            "Implement feature flags",
            "Add metrics collection",
            "Fix cross-site scripting vulnerability",
            "Add email notification service",
            "Implement OAuth2 authentication",
            "Add Docker support",
            "Improve query performance",
            "Add API versioning",
        ]

        authors = [
            ("Alice Developer", "alice@example.com"),
            ("Bob Coder", "bob@example.com"),
            ("Charlie Hacker", "charlie@example.com"),
            ("Diana Engineer", "diana@example.com"),
        ]

        # Start from 30 days ago
        current_time = datetime.now(UTC) - timedelta(days=30)

        for i, message in enumerate(commit_messages):
            # Generate a fake commit hash
            commit_hash = f"{random.randint(0, 0xffffffff):08x}{random.randint(100000, 999999)}"

            # Random author
            author_name, author_email = random.choice(authors)

            # Random diff stats
            diff_stats = DiffStats(
                files_changed=random.randint(1, 15),
                insertions=random.randint(10, 500),
                deletions=random.randint(0, 200),
            )

            # Create commit
            commit = Commit(
                repository_id=repo.id,
                commit_hash=commit_hash,
                message=message,
                author_name=author_name,
                author_email=author_email,
                committer_name=author_name,
                committer_email=author_email,
                committed_at=current_time,
                diff_stats=diff_stats,
            )

            # Check if commit already exists
            existing = await commit_repository.get_by_hash(repo.id, commit_hash)
            if not existing:
                saved_commit = await commit_repository.create(commit)
                print(f"Created commit {i+1}/{len(commit_messages)}: {saved_commit.short_hash} - {message[:50]}")
            else:
                print(f"Skipping existing commit: {commit_hash[:7]}")

            # Move time forward by a random amount (0.5 to 2 days)
            current_time += timedelta(hours=random.randint(12, 48))

        await session.commit()
        print(f"\nDone! Created commits for repository ID: {repo.id}")
        print(f"View them at: http://web.haven.local/repository/{repo.id}/browse")


if __name__ == "__main__":
    asyncio.run(create_sample_commits())
