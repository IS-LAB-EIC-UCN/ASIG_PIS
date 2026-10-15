from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from crisisops_example.core.database import get_db
from crisisops_example.resources.repository import ResourceRepository
from crisisops_example.resources.schemas import ResourceCreate, ResourceRead
from crisisops_example.resources.service import ResourceService


router = APIRouter(prefix="/resources", tags=["resources"])


@router.post(
    "",
    response_model=ResourceRead,
    status_code=status.HTTP_201_CREATED,
)
def register_resource(
    payload: ResourceCreate,
    db: Session = Depends(get_db),
) -> ResourceRead:
    repository = ResourceRepository(db)
    service = ResourceService(repository)
    return service.register(payload)
