# -*- coding: utf-8 -*-
from time import time
from typing import List, Optional
import uuid

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import Field
from enum import Enum
from salver.common.models.fact import BaseFact


class ScanState(str, Enum):
    UNKNOWN = "unknown"
    CREATED = "created"

    STARTING = "starting"
    STARTED = "started"
    FINISHED = "finished"
    ERRORED = "errored"


class ScanConfig(BaseModel):
    class Config(BaseConfig):
        extra = "allow"

class Scan(BaseModel):
    case_id: uuid.UUID
    facts: List[BaseFact] = []
    scan_type: str
    config: ScanConfig

    class Config(BaseConfig):
        extra = "ignore"
        use_enum_values = True


class ScanInRequest(Scan):
    pass

class ScanInDB(Scan):
    timestamp: float = Field(default_factory=time)
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    state: ScanState = ScanState.UNKNOWN

