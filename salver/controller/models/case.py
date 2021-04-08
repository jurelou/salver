# -*- coding: utf-8 -*-
from time import time
import uuid

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import Field
from typing import List

class Case(BaseModel):
    name: str

class CaseInRequest(Case):
    pass

class CaseInResponse(Case):
    scans: List[uuid.UUID] = []

class CaseInDB(Case):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_on: float = Field(default_factory=time)

