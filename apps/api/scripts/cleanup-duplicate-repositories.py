#!/usr/bin/env python
"""Script to clean up duplicate repositories."""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

from haven.infrastructure.database.models import RepositoryModel


async def cleanup_duplicate_repositories():
    """Remove duplicate repositories and keep the correct one."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=True
    )

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        # Delete the repositories with incorrect paths
        # Keep ID 15 which has the correct path /Users/paul/dev/jazzydog-labs/haven
        delete_stmt = delete(RepositoryModel).where(RepositoryModel.id.in_([13, 14]))
        result = await session.execute(delete_stmt)
        
        # Update ID 15 to use "haven" slug
        from sqlalchemy import update
        update_stmt = (
            update(RepositoryModel)
            .where(RepositoryModel.id == 15)
            .values(slug="haven")
        )
        await session.execute(update_stmt)
        
        await session.commit()
        print(f"Deleted {result.rowcount} duplicate repositories")
        print("Updated repository ID 15 to use 'haven' slug")
    
    # Clean up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(cleanup_duplicate_repositories())