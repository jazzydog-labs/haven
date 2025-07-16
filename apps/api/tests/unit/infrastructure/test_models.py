"""Unit tests for SQLAlchemy models."""

from datetime import UTC, datetime
from uuid import uuid4

from haven.domain.entities import Record
from haven.infrastructure.database.models import RecordModel


class TestRecordModel:
    """Test cases for RecordModel."""

    def test_create_record_model(self) -> None:
        """Test creating a RecordModel instance."""
        test_id = uuid4()
        test_data = {"key": "value"}

        model = RecordModel(
            id=test_id,
            data=test_data,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        assert model.id == test_id
        assert model.data == test_data
        assert isinstance(model.created_at, datetime)
        assert isinstance(model.updated_at, datetime)

    def test_model_to_entity_mapping(self) -> None:
        """Test that model fields map correctly to entity."""
        test_id = uuid4()
        test_data = {"key": "value", "number": 42}
        now = datetime.now(UTC)

        model = RecordModel(
            id=test_id,
            data=test_data,
            created_at=now,
            updated_at=now,
        )

        # Create entity from model data
        entity = Record(
            id=model.id,
            data=model.data,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        assert entity.id == model.id
        assert entity.data == model.data
        assert entity.created_at == model.created_at
        assert entity.updated_at == model.updated_at

    def test_repr(self) -> None:
        """Test string representation of RecordModel."""
        test_id = uuid4()
        now = datetime.now(UTC)

        model = RecordModel(
            id=test_id,
            data={},
            created_at=now,
            updated_at=now,
        )

        repr_str = repr(model)
        assert f"RecordModel(id={test_id}" in repr_str
        assert "created_at=" in repr_str
