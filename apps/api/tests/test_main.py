"""Test main module."""

import pytest

from haven import __version__


def test_version() -> None:
    """Test version is set correctly."""
    assert __version__ == "0.1.0"


@pytest.mark.asyncio
async def test_placeholder() -> None:
    """Placeholder test for async functionality."""
    # TODO: Add real tests when main.py is implemented
    assert True
