#!/usr/bin/env python
"""Script to fix repository paths for Docker environment."""

import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from haven.infrastructure.database.models import RepositoryModel


async def fix_repository_paths():
    """Update repository paths to work in Docker container."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=True
    )

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Check if running in Docker
    is_docker = os.path.exists("/.dockerenv") or os.environ.get("RUNNING_IN_DOCKER")
    
    async with async_session_maker() as session:
        # Update Haven repository path
        if is_docker:
            # In Docker, use mounted path
            update_stmt = (
                update(RepositoryModel)
                .where(RepositoryModel.slug == "haven")
                .values(url="/repo")
            )
        else:
            # On host, use actual path
            import pathlib
            haven_path = str(pathlib.Path(__file__).parent.parent.parent.parent.absolute())
            update_stmt = (
                update(RepositoryModel)
                .where(RepositoryModel.slug == "haven")
                .values(url=haven_path)
            )
        
        result = await session.execute(update_stmt)
        await session.commit()
        
        print(f"Updated {result.rowcount} repository paths")
        print(f"Docker environment: {is_docker}")
    
    # Clean up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(fix_repository_paths())