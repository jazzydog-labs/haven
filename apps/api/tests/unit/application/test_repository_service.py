from unittest.mock import AsyncMock, Mock

import pytest

from haven.application.services.repository_service import RepositoryService
from haven.domain.entities.repository import Repository


@pytest.mark.asyncio
async def test_create_repository():
    mock_repo = Mock()
    mock_repo.create = AsyncMock()

    service = RepositoryService(mock_repo)

    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False,
    )
    mock_repo.create.return_value = repository

    result = await service.create_repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False,
    )

    assert result.name == "test-repo"
    assert result.full_name == "user/test-repo"
    assert result.url == "https://github.com/user/test-repo.git"
    assert result.branch == "main"
    assert result.is_local is False
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_repository_by_id():
    mock_repo = Mock()
    mock_repo.get_by_id = AsyncMock()

    service = RepositoryService(mock_repo)

    repository = Repository(
        id=1,
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False,
    )
    mock_repo.get_by_id.return_value = repository

    result = await service.get_repository_by_id(1)

    assert result.id == 1
    assert result.name == "test-repo"
    mock_repo.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_repository_by_name():
    mock_repo = Mock()
    mock_repo.get_by_name = AsyncMock()

    service = RepositoryService(mock_repo)

    repository = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False,
    )
    mock_repo.get_by_name.return_value = repository

    result = await service.get_repository_by_name("test-repo")

    assert result.name == "test-repo"
    mock_repo.get_by_name.assert_called_once_with("test-repo")


@pytest.mark.asyncio
async def test_get_all_repositories():
    mock_repo = Mock()
    mock_repo.get_all = AsyncMock()

    service = RepositoryService(mock_repo)

    repositories = [
        Repository(
            name="repo1",
            full_name="user/repo1",
            url="https://github.com/user/repo1.git",
            branch="main",
            is_local=False,
        ),
        Repository(
            name="repo2",
            full_name="user/repo2",
            url="https://github.com/user/repo2.git",
            branch="main",
            is_local=False,
        ),
    ]
    mock_repo.get_all.return_value = repositories

    result = await service.get_all_repositories()

    assert len(result) == 2
    assert result[0].name == "repo1"
    assert result[1].name == "repo2"
    mock_repo.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_update_repository():
    mock_repo = Mock()
    mock_repo.get_by_id = AsyncMock()
    mock_repo.update = AsyncMock()

    service = RepositoryService(mock_repo)

    repository = Repository(
        id=1,
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False,
    )
    updated_repository = Repository(
        id=1,
        name="updated-repo",
        full_name="user/updated-repo",
        url="https://github.com/user/test-repo.git",
        branch="develop",
        is_local=False,
    )

    mock_repo.get_by_id.return_value = repository
    mock_repo.update.return_value = updated_repository

    result = await service.update_repository(
        1, name="updated-repo", full_name="user/updated-repo", branch="develop"
    )

    assert result.name == "updated-repo"
    assert result.full_name == "user/updated-repo"
    assert result.branch == "develop"
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_repository_not_found():
    mock_repo = Mock()
    mock_repo.get_by_id = AsyncMock()
    mock_repo.get_by_id.return_value = None

    service = RepositoryService(mock_repo)

    with pytest.raises(ValueError, match="Repository with id 1 not found"):
        await service.update_repository(1, name="updated-repo")


@pytest.mark.asyncio
async def test_delete_repository():
    mock_repo = Mock()
    mock_repo.delete = AsyncMock()
    mock_repo.delete.return_value = True

    service = RepositoryService(mock_repo)

    result = await service.delete_repository(1)

    assert result is True
    mock_repo.delete.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_validate_repository_path():
    mock_repo = Mock()
    service = RepositoryService(mock_repo)

    # Test local repository with existing path
    local_repo = Repository(
        name="test-repo",
        full_name="test-repo",
        url="/Users/paul/dev/jazzydog-labs/haven",
        branch="main",
        is_local=True,
    )

    result = service.validate_repository_path(local_repo)
    assert result is True

    # Test remote repository (should always return True)
    remote_repo = Repository(
        name="test-repo",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo.git",
        branch="main",
        is_local=False,
    )

    result = service.validate_repository_path(remote_repo)
    assert result is True
