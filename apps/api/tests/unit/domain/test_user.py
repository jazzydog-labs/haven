import pytest

from haven.domain.entities.user import User


def test_user_creation():
    user = User(username="plva", email="paul@example.com", display_name="Paul")

    assert user.username == "plva"
    assert user.email == "paul@example.com"
    assert user.display_name == "Paul"
    assert user.avatar_url is None
    assert user.id is None


def test_user_creation_with_avatar():
    user = User(
        username="plva",
        email="paul@example.com",
        display_name="Paul",
        avatar_url="https://example.com/avatar.jpg",
    )

    assert user.avatar_url == "https://example.com/avatar.jpg"


def test_user_validation():
    with pytest.raises(ValueError, match="Username cannot be empty"):
        User(username="", email="test@example.com", display_name="Test")

    with pytest.raises(ValueError, match="Email cannot be empty"):
        User(username="test", email="", display_name="Test")

    with pytest.raises(ValueError, match="Invalid email format"):
        User(username="test", email="invalid-email", display_name="Test")


def test_user_display_name_defaults_to_username():
    user = User(username="plva", email="paul@example.com", display_name="")

    assert user.display_name == "plva"
