from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ResourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: str = Field(min_length=1, max_length=50)
    location: str | None = Field(default=None, max_length=150)


class ResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    status: str
    location: str | None
