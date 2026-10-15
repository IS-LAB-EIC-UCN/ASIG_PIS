from __future__ import annotations

from crisisops_example.resources.models import Resource
from crisisops_example.resources.repository import ResourceRepository
from crisisops_example.resources.schemas import ResourceCreate


INITIAL_RESOURCE_STATUS = "AVAILABLE"


class ResourceService:
    def __init__(self, repository: ResourceRepository):
        self.repository = repository

    def register(self, data: ResourceCreate) -> Resource:
        # Regla de negocio del ejemplo:
        # todo recurso nuevo comienza en AVAILABLE.
        resource = Resource(
            name=data.name,
            type=data.type,
            status=INITIAL_RESOURCE_STATUS,
            location=data.location,
        )
        return self.repository.save(resource)
