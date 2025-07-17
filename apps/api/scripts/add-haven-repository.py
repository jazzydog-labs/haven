#!/usr/bin/env python
"""Script to add the Haven repository itself to the database."""

import asyncio
import hashlib
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from haven.infrastructure.database.repositories.repository_repository import (
    RepositoryRepositoryImpl,
)
from haven.domain.entities.repository import Repository
from haven.infrastructure.git.git_client import GitClient


async def add_haven_repository():
    """Add the Haven repository to the database."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=False
    )

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        repo_impl = RepositoryRepositoryImpl(session)
        
        # Path to Haven repository (go up three directories from scripts/add-haven-repository.py)
        haven_path = str(Path(__file__).parent.parent.parent.parent.absolute())
        
        # Check if already exists
        existing = await repo_impl.get_by_url(haven_path)
        if existing:
            print(f"Repository already exists with hash: {existing.repository_hash}")
            return
        
        # Get remote URL
        git_client = GitClient()
        remote_url = await git_client.get_remote_url(haven_path)
        
        # Create repository
        repository = Repository(
            name="haven",
            full_name="Haven - Git Diff Visualization Platform",
            url=haven_path,
            remote_url=remote_url,
            branch="main",
            description="A platform for visualizing and reviewing git diffs with a clean architecture",
            is_local=True,
            slug="haven"  # Use simple slug for Haven itself
        )
        
        # Generate hash
        repository.repository_hash = hashlib.sha256(haven_path.encode()).hexdigest()
        
        # Save to database
        saved_repo = await repo_impl.create(repository)
        await session.commit()
        
        print(f"Haven repository added successfully!")
        print(f"Repository ID: {saved_repo.id}")
        print(f"Repository Slug: {saved_repo.slug}")
        print(f"Repository Hash: {saved_repo.repository_hash}")
        print(f"Local Path: {saved_repo.url}")
        print(f"Remote URL: {saved_repo.remote_url}")
        print(f"\nAccess it at: http://haven.local/repository/{saved_repo.slug or saved_repo.repository_hash}/browse")
    
    # Clean up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(add_haven_repository())