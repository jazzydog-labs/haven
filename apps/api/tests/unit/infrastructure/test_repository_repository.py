import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from haven.domain.entities.repository import Repository
from haven.infrastructure.database.repositories.repository_repository import RepositoryRepositoryImpl

@pytest.mark.asyncio
async def test_create_repository(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        description="Test repository",
        is_local=False
    )
    
    created_repo = await repo.create(repository)
    
    assert created_repo.id is not None
    assert created_repo.name == "test-repo"
    assert created_repo.full_name == "user/test-repo"
    assert created_repo.url == "https://github.com/user/test-repo.git"
    assert created_repo.branch == "main"
    assert created_repo.description == "Test repository"
    assert created_repo.is_local is False
    assert created_repo.created_at is not None
    assert created_repo.updated_at is not None

@pytest.mark.asyncio
async def test_get_repository_by_id(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False
    )
    
    created_repo = await repo.create(repository)
    found_repo = await repo.get_by_id(created_repo.id)
    
    assert found_repo is not None
    assert found_repo.id == created_repo.id
    assert found_repo.name == "test-repo"

@pytest.mark.asyncio
async def test_get_repository_by_name(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False
    )
    
    await repo.create(repository)
    found_repo = await repo.get_by_name("test-repo")
    
    assert found_repo is not None
    assert found_repo.name == "test-repo"

@pytest.mark.asyncio
async def test_get_repository_by_url(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False
    )
    
    await repo.create(repository)
    found_repo = await repo.get_by_url("https://github.com/user/test-repo.git")
    
    assert found_repo is not None
    assert found_repo.url == "https://github.com/user/test-repo.git"

@pytest.mark.asyncio
async def test_get_all_repositories(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repo1 = Repository(
        name="repo1",
        full_name="user/repo1",
        url="https://github.com/user/repo1.git",
        branch="main",
        is_local=False
    )
    repo2 = Repository(
        name="repo2",
        full_name="user/repo2",
        url="https://github.com/user/repo2.git",
        branch="main",
        is_local=False
    )
    
    await repo.create(repo1)
    await repo.create(repo2)
    
    repositories = await repo.get_all()
    
    assert len(repositories) == 2
    repo_names = [r.name for r in repositories]
    assert "repo1" in repo_names
    assert "repo2" in repo_names

@pytest.mark.asyncio
async def test_update_repository(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False
    )
    
    created_repo = await repo.create(repository)
    created_repo.description = "Updated description"
    created_repo.branch = "develop"
    
    updated_repo = await repo.update(created_repo)
    
    assert updated_repo.description == "Updated description"
    assert updated_repo.branch == "develop"

@pytest.mark.asyncio
async def test_delete_repository(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False
    )
    
    created_repo = await repo.create(repository)
    result = await repo.delete(created_repo.id)
    
    assert result is True
    
    deleted_repo = await repo.get_by_id(created_repo.id)
    assert deleted_repo is None

@pytest.mark.asyncio
async def test_update_repository_not_found(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    repository = Repository(
        id=999,
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False
    )
    
    with pytest.raises(ValueError, match="Repository with id 999 not found"):
        await repo.update(repository)

@pytest.mark.asyncio
async def test_delete_repository_not_found(test_session: AsyncSession):
    repo = RepositoryRepositoryImpl(test_session)
    
    result = await repo.delete(999)
    assert result is False