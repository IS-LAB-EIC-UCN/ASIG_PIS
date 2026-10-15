from __future__ import annotations

from sqlalchemy.orm import Session

from crisisops_example.resources.models import Resource


class ResourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, resource: Resource) -> Resource:
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get_by_id(self, resource_id: int) -> Resource | None:
        return self.db.get(Resource, resource_id)
