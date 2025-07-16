"""Pytest configuration and fixtures."""

import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from haven.domain.entities import Record
from haven.infrastructure.database.models import Base, RecordModel  # noqa: F401
from haven.infrastructure.database.session import create_session_factory


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create test database engine."""
    # Use in-memory SQLite for tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=NullPool,
        echo=False,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = create_session_factory(test_engine)

    async with (
        async_session() as session,
        session.begin(),
    ):
        yield session
        # Transaction will be rolled back automatically


@pytest.fixture
def anyio_backend() -> str:
    """Configure anyio backend for async tests."""
    return "asyncio"


@pytest.fixture
def sample_record() -> Record:
    """Create a sample record for testing."""
    return Record(data={"test": "data", "value": 42})


@pytest.fixture
def test_client() -> Generator:
    """Create test client with in-memory test database."""
    import os
    from fastapi.testclient import TestClient
    from haven.interface.api.app import create_app
    
    # Set test database URL - async sqlite URL that works with string IDs
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
    
    # Create app
    app = create_app()
    
    # Create test client
    with TestClient(app) as client:
        # Initialize database with tables
        import asyncio
        from sqlalchemy import create_engine
        from haven.infrastructure.database.models import Base
        
        # Create tables using sync engine for simplicity
        engine = create_engine("sqlite:///./test.db")
        Base.metadata.create_all(engine)
        engine.dispose()
        
        yield client
        
        # Cleanup
        import os
        if os.path.exists("test.db"):
            os.remove("test.db")
