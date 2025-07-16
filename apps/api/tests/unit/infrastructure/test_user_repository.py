import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from haven.domain.entities.user import User
from haven.infrastructure.database.repositories.user_repository import UserRepositoryImpl

@pytest.mark.asyncio
async def test_create_user(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    created_user = await repo.create(user)
    
    assert created_user.id is not None
    assert created_user.username == "testuser"
    assert created_user.email == "test@example.com"
    assert created_user.display_name == "Test User"
    assert created_user.created_at is not None
    assert created_user.updated_at is not None

@pytest.mark.asyncio
async def test_get_user_by_id(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    created_user = await repo.create(user)
    found_user = await repo.get_by_id(created_user.id)
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.username == "testuser"

@pytest.mark.asyncio
async def test_get_user_by_username(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    await repo.create(user)
    found_user = await repo.get_by_username("testuser")
    
    assert found_user is not None
    assert found_user.username == "testuser"

@pytest.mark.asyncio
async def test_get_user_by_email(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    await repo.create(user)
    found_user = await repo.get_by_email("test@example.com")
    
    assert found_user is not None
    assert found_user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_all_users(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user1 = User(username="user1", email="user1@example.com", display_name="User 1")
    user2 = User(username="user2", email="user2@example.com", display_name="User 2")
    
    await repo.create(user1)
    await repo.create(user2)
    
    users = await repo.get_all()
    
    assert len(users) == 2
    usernames = [u.username for u in users]
    assert "user1" in usernames
    assert "user2" in usernames

@pytest.mark.asyncio
async def test_update_user(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    created_user = await repo.create(user)
    created_user.display_name = "Updated User"
    created_user.avatar_url = "https://example.com/avatar.jpg"
    
    updated_user = await repo.update(created_user)
    
    assert updated_user.display_name == "Updated User"
    assert updated_user.avatar_url == "https://example.com/avatar.jpg"

@pytest.mark.asyncio
async def test_delete_user(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User"
    )
    
    created_user = await repo.create(user)
    result = await repo.delete(created_user.id)
    
    assert result is True
    
    deleted_user = await repo.get_by_id(created_user.id)
    assert deleted_user is None

@pytest.mark.asyncio
async def test_duplicate_username_raises_error(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user1 = User(username="testuser", email="test1@example.com", display_name="Test User 1")
    user2 = User(username="testuser", email="test2@example.com", display_name="Test User 2")
    
    await repo.create(user1)
    
    with pytest.raises(ValueError, match="Username or email already exists"):
        await repo.create(user2)

@pytest.mark.asyncio
async def test_duplicate_email_raises_error(test_session: AsyncSession):
    repo = UserRepositoryImpl(test_session)
    
    user1 = User(username="user1", email="test@example.com", display_name="Test User 1")
    user2 = User(username="user2", email="test@example.com", display_name="Test User 2")
    
    await repo.create(user1)
    
    with pytest.raises(ValueError, match="Username or email already exists"):
        await repo.create(user2)