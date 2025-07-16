"""GraphQL schema definition."""

from datetime import datetime
from typing import Optional
from uuid import UUID

import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info

from haven.application.services import RecordService
from haven.domain.entities import Record
from haven.domain.unit_of_work import UnitOfWork
from haven.infrastructure.database.factory import db_factory


@strawberry.type
class RecordType:
    """GraphQL type for Record."""

    id: UUID
    data: JSON
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, record: Record) -> "RecordType":
        """Create GraphQL type from domain entity."""
        return cls(
            id=record.id,
            data=record.data,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )


@strawberry.type
class RecordConnection:
    """Relay-style connection for records."""

    edges: list["RecordEdge"]
    page_info: "PageInfo"


@strawberry.type
class RecordEdge:
    """Edge in record connection."""

    cursor: str
    node: RecordType


@strawberry.type
class PageInfo:
    """Page information for pagination."""

    has_next_page: bool
    end_cursor: Optional[str]


@strawberry.input
class RecordInput:
    """Input type for creating/updating records."""

    data: JSON


async def get_service(info: Info) -> RecordService:
    """Get record service from context."""
    # In production, this would come from dependency injection
    async for uow in db_factory.get_unit_of_work():
        return RecordService(uow)


@strawberry.type
class Query:
    """Root query type."""

    @strawberry.field
    async def record(self, info: Info, id: UUID) -> Optional[RecordType]:
        """Get a single record by ID."""
        service = await get_service(info)
        try:
            record = await service.get_record(id)
            return RecordType.from_entity(record)
        except Exception:
            return None

    @strawberry.field
    async def records(
        self,
        info: Info,
        first: int = 25,
        after: Optional[str] = None,
    ) -> RecordConnection:
        """List records with cursor-based pagination."""
        service = await get_service(info)
        
        # Decode cursor to offset
        offset = 0
        if after:
            try:
                offset = int(after)
            except ValueError:
                offset = 0
        
        # Get records
        records, total = await service.list_records(limit=first + 1, offset=offset)
        
        # Check if there are more records
        has_next = len(records) > first
        if has_next:
            records = records[:first]
        
        # Create edges
        edges = []
        for i, record in enumerate(records):
            cursor = str(offset + i)
            edges.append(
                RecordEdge(
                    cursor=cursor,
                    node=RecordType.from_entity(record),
                )
            )
        
        # Create page info
        end_cursor = edges[-1].cursor if edges else None
        page_info = PageInfo(
            has_next_page=has_next,
            end_cursor=end_cursor,
        )
        
        return RecordConnection(edges=edges, page_info=page_info)


@strawberry.type
class Mutation:
    """Root mutation type."""

    @strawberry.mutation
    async def create_record(self, info: Info, input: RecordInput) -> RecordType:
        """Create a new record."""
        service = await get_service(info)
        record = await service.create_record(input.data)
        return RecordType.from_entity(record)

    @strawberry.mutation
    async def update_record(
        self, info: Info, id: UUID, input: RecordInput
    ) -> RecordType:
        """Update an existing record."""
        service = await get_service(info)
        record = await service.update_record(id, input.data)
        return RecordType.from_entity(record)

    @strawberry.mutation
    async def delete_record(self, info: Info, id: UUID) -> bool:
        """Delete a record by ID."""
        service = await get_service(info)
        return await service.delete_record(id)


# Create the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)