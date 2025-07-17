#!/usr/bin/env python
"""Script to set the 'haven' slug for the correct repository."""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from haven.infrastructure.database.models import RepositoryModel


async def set_haven_slug():
    """Set the 'haven' slug for the correct repository."""
    # Database connection
    engine = create_async_engine(
        "postgresql+asyncpg://haven:haven@localhost:5432/haven",
        echo=True
    )

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        # Update ID 15 to use "haven" slug
        update_stmt = (
            update(RepositoryModel)
            .where(RepositoryModel.id == 15)
            .values(slug="haven")
        )
        await session.execute(update_stmt)
        
        await session.commit()
        print("Updated repository ID 15 to use 'haven' slug")
    
    # Clean up
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(set_haven_slug())