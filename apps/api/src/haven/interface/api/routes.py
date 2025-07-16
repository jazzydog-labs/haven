"""API routes for REST endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from haven.application.dtos import (
    RecordCreateDTO,
    RecordResponseDTO,
    RecordUpdateDTO,
)
from haven.application.dtos.record_dtos import RecordListResponseDTO
from haven.application.services import RecordService
from haven.domain.entities import Record
from haven.domain.unit_of_work import UnitOfWork
from haven.infrastructure.database.factory import db_factory

router = APIRouter(tags=["Records"])


async def get_unit_of_work() -> UnitOfWork:
    """Dependency to get unit of work."""
    async for uow in db_factory.get_unit_of_work():
        yield uow


def get_record_service(uow: UnitOfWork = Depends(get_unit_of_work)) -> RecordService:
    """Dependency to get record service."""
    return RecordService(uow)


def record_to_response(record: Record) -> RecordResponseDTO:
    """Convert domain entity to response DTO."""
    return RecordResponseDTO(
        id=record.id,
        data=record.data,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.post("/records", response_model=RecordResponseDTO, status_code=201)
async def create_record(
    dto: RecordCreateDTO,
    service: RecordService = Depends(get_record_service),
) -> RecordResponseDTO:
    """Create a new record."""
    record = await service.create_record(dto.data)
    return record_to_response(record)


@router.get("/records/{record_id}", response_model=RecordResponseDTO)
async def get_record(
    record_id: UUID,
    service: RecordService = Depends(get_record_service),
) -> RecordResponseDTO:
    """Get a record by ID."""
    record = await service.get_record(record_id)
    return record_to_response(record)


@router.get("/records", response_model=RecordListResponseDTO)
async def list_records(
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    service: RecordService = Depends(get_record_service),
) -> RecordListResponseDTO:
    """List records with pagination."""
    records, total = await service.list_records(limit=limit, offset=offset)

    return RecordListResponseDTO(
        items=[record_to_response(r) for r in records],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.put("/records/{record_id}", response_model=RecordResponseDTO)
async def update_record(
    record_id: UUID,
    dto: RecordUpdateDTO,
    service: RecordService = Depends(get_record_service),
) -> RecordResponseDTO:
    """Update a record completely."""
    record = await service.update_record(record_id, dto.data)
    return record_to_response(record)


@router.patch("/records/{record_id}", response_model=RecordResponseDTO)
async def partial_update_record(
    record_id: UUID,
    dto: dict,  # Allow any partial data
    service: RecordService = Depends(get_record_service),
) -> RecordResponseDTO:
    """Partially update a record."""
    record = await service.partial_update_record(record_id, dto)
    return record_to_response(record)


@router.delete("/records/{record_id}", status_code=204)
async def delete_record(
    record_id: UUID,
    service: RecordService = Depends(get_record_service),
) -> None:
    """Delete a record."""
    deleted = await service.delete_record(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")


@router.head("/records/{record_id}")
async def check_record_exists(
    record_id: UUID,
    service: RecordService = Depends(get_record_service),
) -> None:
    """Check if a record exists."""
    exists = await service.record_exists(record_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Record not found")
