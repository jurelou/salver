# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

from pydantic import BaseModel


class UUIDInResponse(BaseModel):
    id: UUID


class UUIDsInResponse(BaseModel):
    ids: List[UUID]
