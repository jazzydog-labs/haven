"""Test fixtures for Haven."""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest
from faker import Faker

from haven.domain.entities import Record

fake = Faker()


@pytest.fixture
def sample_record_data() -> dict[str, Any]:
    """Generate sample record data."""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "description": fake.text(max_nb_chars=200),
        "count": fake.random_int(min=1, max=100),
        "active": fake.boolean(),
        "metadata": {
            "created_by": fake.user_name(),
            "tags": fake.words(nb=3),
        },
    }


@pytest.fixture
def sample_record(sample_record_data: dict[str, Any]) -> Record:
    """Create a sample Record entity."""
    return Record(
        id=uuid4(),
        data=sample_record_data,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def sample_records(sample_record_data: dict[str, Any]) -> list[Record]:
    """Create multiple sample Record entities."""
    records = []
    for i in range(5):
        data = sample_record_data.copy()
        data["index"] = i
        records.append(
            Record(
                id=uuid4(),
                data=data,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
        )
    return records