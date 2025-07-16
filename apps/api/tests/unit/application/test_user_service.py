import pytest
from unittest.mock import AsyncMock, Mock
from haven.application.services.user_service import UserService
from haven.domain.entities.user import User

@pytest.mark.asyncio
async def test_create_user():
    mock_repo = Mock()
    mock_repo.create = AsyncMock()
    
    service = UserService(mock_repo)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    mock_repo.create.return_value = user
    
    result = await service.create_user(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.display_name == "Test User"
    mock_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_by_id():
    mock_repo = Mock()
    mock_repo.get_by_id = AsyncMock()
    
    service = UserService(mock_repo)
    
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    mock_repo.get_by_id.return_value = user
    
    result = await service.get_user_by_id(1)
    
    assert result.id == 1
    assert result.username == "testuser"
    mock_repo.get_by_id.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_user_by_username():
    mock_repo = Mock()
    mock_repo.get_by_username = AsyncMock()
    
    service = UserService(mock_repo)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    mock_repo.get_by_username.return_value = user
    
    result = await service.get_user_by_username("testuser")
    
    assert result.username == "testuser"
    mock_repo.get_by_username.assert_called_once_with("testuser")

@pytest.mark.asyncio
async def test_get_all_users():
    mock_repo = Mock()
    mock_repo.get_all = AsyncMock()
    
    service = UserService(mock_repo)
    
    users = [
        User(username="user1", email="user1@example.com", display_name="User 1"),
        User(username="user2", email="user2@example.com", display_name="User 2")
    ]
    mock_repo.get_all.return_value = users
    
    result = await service.get_all_users()
    
    assert len(result) == 2
    assert result[0].username == "user1"
    assert result[1].username == "user2"
    mock_repo.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_update_user():
    mock_repo = Mock()
    mock_repo.get_by_id = AsyncMock()
    mock_repo.update = AsyncMock()
    
    service = UserService(mock_repo)
    
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    updated_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        display_name="Updated User"
    )
    
    mock_repo.get_by_id.return_value = user
    mock_repo.update.return_value = updated_user
    
    result = await service.update_user(1, display_name="Updated User")
    
    assert result.display_name == "Updated User"
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_not_found():
    mock_repo = Mock()
    mock_repo.get_by_id = AsyncMock()
    mock_repo.get_by_id.return_value = None
    
    service = UserService(mock_repo)
    
    with pytest.raises(ValueError, match="User with id 1 not found"):
        await service.update_user(1, display_name="Updated User")

@pytest.mark.asyncio
async def test_delete_user():
    mock_repo = Mock()
    mock_repo.delete = AsyncMock()
    mock_repo.delete.return_value = True
    
    service = UserService(mock_repo)
    
    result = await service.delete_user(1)
    
    assert result is True
    mock_repo.delete.assert_called_once_with(1)