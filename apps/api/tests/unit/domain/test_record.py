"""Unit tests for Record entity."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from haven.domain.entities import Record


@pytest.mark.unit
class TestRecord:
    """Test cases for Record entity."""

    def test_create_record_with_defaults(self) -> None:
        """Test creating a record with default values."""
        record = Record()

        assert isinstance(record.id, UUID)
        assert record.data == {}
        assert isinstance(record.created_at, datetime)
        assert isinstance(record.updated_at, datetime)
        assert record.created_at.tzinfo == UTC
        assert record.updated_at.tzinfo == UTC

    def test_create_record_with_data(self) -> None:
        """Test creating a record with specific data."""
        test_data = {"key": "value", "number": 42}
        record = Record(data=test_data)

        assert record.data == test_data
        assert record.data is not test_data  # Ensure it's not the same reference

    def test_create_record_with_id(self) -> None:
        """Test creating a record with specific ID."""
        test_id = uuid4()
        record = Record(id=test_id)

        assert record.id == test_id

    def test_invalid_data_type_raises_error(self) -> None:
        """Test that non-dict data raises ValueError."""
        with pytest.raises(ValueError, match="Record data must be a dictionary"):
            Record(data="not a dict")  # type: ignore

    def test_update_data(self) -> None:
        """Test updating record data."""
        record = Record(data={"old": "data"})
        original_updated_at = record.updated_at

        new_data = {"new": "data"}
        record.update_data(new_data)

        assert record.data == new_data
        assert record.updated_at > original_updated_at

    def test_update_data_invalid_type(self) -> None:
        """Test that update_data with non-dict raises ValueError."""
        record = Record()

        with pytest.raises(ValueError, match="New data must be a dictionary"):
            record.update_data("not a dict")  # type: ignore

    def test_merge_data(self) -> None:
        """Test merging partial data into record."""
        record = Record(data={"existing": "value", "number": 1})
        original_updated_at = record.updated_at

        partial_data = {"number": 2, "new": "field"}
        record.merge_data(partial_data)

        assert record.data == {"existing": "value", "number": 2, "new": "field"}
        assert record.updated_at > original_updated_at

    def test_merge_data_invalid_type(self) -> None:
        """Test that merge_data with non-dict raises ValueError."""
        record = Record()

        with pytest.raises(ValueError, match="Partial data must be a dictionary"):
            record.merge_data("not a dict")  # type: ignore

    def test_to_dict(self) -> None:
        """Test converting record to dictionary."""
        test_id = uuid4()
        test_data = {"key": "value"}
        record = Record(id=test_id, data=test_data)

        result = record.to_dict()

        assert result["id"] == str(test_id)
        assert result["data"] == test_data
        assert "created_at" in result
        assert "updated_at" in result
        # Verify ISO format
        datetime.fromisoformat(result["created_at"])
        datetime.fromisoformat(result["updated_at"])

    def test_equality_same_id(self) -> None:
        """Test that records with same ID are equal."""
        test_id = uuid4()
        record1 = Record(id=test_id, data={"a": 1})
        record2 = Record(id=test_id, data={"b": 2})

        assert record1 == record2

    def test_equality_different_id(self) -> None:
        """Test that records with different IDs are not equal."""
        record1 = Record(data={"same": "data"})
        record2 = Record(data={"same": "data"})

        assert record1 != record2

    def test_equality_non_record(self) -> None:
        """Test equality with non-Record object."""
        record = Record()

        assert record != "not a record"
        assert record != 123
        assert record is not None

    def test_hash(self) -> None:
        """Test that records can be used in sets/dicts."""
        record1 = Record()
        record2 = Record()
        record3 = Record(id=record1.id)  # Same ID as record1

        record_set = {record1, record2, record3}

        assert len(record_set) == 2  # record3 should be considered same as record1

    def test_timezone_naive_conversion(self) -> None:
        """Test that timezone-naive datetimes are converted to UTC."""
        naive_dt = datetime(2023, 1, 1, 12, 0, 0)
        record = Record(created_at=naive_dt, updated_at=naive_dt)

        assert record.created_at.tzinfo == UTC
        assert record.updated_at.tzinfo == UTC
