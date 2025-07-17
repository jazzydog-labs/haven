import pytest

from haven.domain.entities.repository import Repository


def test_repository_creation():
    repo = Repository(
        name="haven",
        full_name="jazzydog-labs/haven",
        url="/Users/paul/dev/jazzydog-labs/haven",
        branch="main",
        description="Haven repository",
        is_local=True,
    )
    assert repo.name == "haven"
    assert repo.full_name == "jazzydog-labs/haven"
    assert repo.url == "/Users/paul/dev/jazzydog-labs/haven"
    assert repo.branch == "main"
    assert repo.description == "Haven repository"
    assert repo.is_local is True


def test_repository_validation():
    with pytest.raises(ValueError, match="Repository name cannot be empty"):
        Repository(name="", full_name="test", url="/path", branch="main")

    with pytest.raises(ValueError, match="Repository URL cannot be empty"):
        Repository(name="test", full_name="test", url="", branch="main")

    with pytest.raises(ValueError, match="Branch cannot be empty"):
        Repository(name="test", full_name="test", url="/path", branch="")


def test_repository_local_path_validation():
    with pytest.raises(ValueError, match="Local repository path does not exist"):
        Repository(
            name="test", full_name="test", url="/nonexistent/path", branch="main", is_local=True
        )


def test_repository_display_name_property():
    repo = Repository(
        name="haven",
        full_name="jazzydog-labs/haven",
        url="/Users/paul/dev/jazzydog-labs/haven",
        branch="main",
    )
    assert repo.display_name == "jazzydog-labs/haven"

    repo_no_full_name = Repository(
        name="haven", full_name="", url="/Users/paul/dev/jazzydog-labs/haven", branch="main"
    )
    assert repo_no_full_name.display_name == "haven"


def test_repository_is_github_property():
    github_repo = Repository(
        name="test",
        full_name="user/test",
        url="https://github.com/user/test.git",
        branch="main",
        is_local=False,
    )
    assert github_repo.is_github is True

    local_repo = Repository(
        name="test",
        full_name="test",
        url="/Users/paul/dev/jazzydog-labs/haven",
        branch="main",
        is_local=True,
    )
    assert local_repo.is_github is False


def test_repository_remote_creation():
    repo = Repository(
        name="test",
        full_name="user/test",
        url="https://github.com/user/test.git",
        branch="main",
        is_local=False,
    )
    assert repo.is_local is False
    assert repo.is_github is True
