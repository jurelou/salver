from pydantic import BaseModel
from uuid import UUID
from typing import List

class UUIDInResponse(BaseModel):
    id: UUID

class UUIDsInResponse(BaseModel):
    ids: List[UUID]
