#!/usr/bin/env python3
"""Script to update repository hashes for existing repositories."""

import asyncio
import hashlib
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from haven.infrastructure.database.factory import db_factory
from haven.infrastructure.database.models import RepositoryModel
from haven.infrastructure.git.git_client import GitClient


async def update_repository_hashes():
    """Update repository hashes and remote URLs for existing repositories."""
    await db_factory.init()
    
    async with db_factory.get_session() as session:
        # Get all repositories
        stmt = select(RepositoryModel)
        result = await session.execute(stmt)
        repositories = result.scalars().all()
        
        git_client = GitClient()
        
        for repo in repositories:
            print(f"Processing repository: {repo.name}")
            
            # Generate hash if not present
            if not repo.repository_hash:
                repo.repository_hash = hashlib.sha256(repo.url.encode()).hexdigest()
                print(f"  Generated hash: {repo.repository_hash}")
            
            # Try to get remote URL if not present
            if not repo.remote_url and repo.is_local:
                try:
                    remote_url = await git_client.get_remote_url(repo.url)
                    if remote_url:
                        repo.remote_url = remote_url
                        print(f"  Found remote URL: {remote_url}")
                except Exception as e:
                    print(f"  Could not get remote URL: {e}")
            
            session.add(repo)
        
        await session.commit()
        print("\nAll repositories updated!")


if __name__ == "__main__":
    asyncio.run(update_repository_hashes())