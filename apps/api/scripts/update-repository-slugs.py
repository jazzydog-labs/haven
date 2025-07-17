#!/usr/bin/env python
"""Script to update existing repositories with slugs."""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

from haven.infrastructure.database.models import RepositoryModel


async def update_repository_slugs():
    """Update existing repositories with slugs."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=True
    )

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        # Get all repositories
        stmt = select(RepositoryModel)
        result = await session.execute(stmt)
        repositories = result.scalars().all()
        
        # Track used slugs
        used_slugs = set()
        
        for repo in repositories:
            if repo.slug:
                used_slugs.add(repo.slug)
                continue
                
            # Try to use repository name as slug
            slug = repo.name.lower()
            
            # If name is already used, use short hash
            if slug in used_slugs:
                slug = repo.repository_hash[:8] if repo.repository_hash else f"repo-{repo.id}"
            
            used_slugs.add(slug)
            
            # Update the repository
            update_stmt = (
                update(RepositoryModel)
                .where(RepositoryModel.id == repo.id)
                .values(slug=slug)
            )
            await session.execute(update_stmt)
            
            print(f"Updated repository '{repo.name}' (ID: {repo.id}) with slug: {slug}")
        
        await session.commit()
        print(f"\nUpdated {len(repositories)} repositories with slugs")
    
    # Clean up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(update_repository_slugs())