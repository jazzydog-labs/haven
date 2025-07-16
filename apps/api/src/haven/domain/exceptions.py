"""Domain-specific exceptions."""


class DomainError(Exception):
    """Base exception for domain errors."""

    pass


class RecordNotFoundError(DomainError):
    """Raised when a record is not found."""

    def __init__(self, record_id: str) -> None:
        super().__init__(f"Record with ID {record_id} not found")
        self.record_id = record_id


class InvalidRecordDataError(DomainError):
    """Raised when record data is invalid."""

    pass