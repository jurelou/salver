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


class ScanResult(BaseModel):
    duration: float
    executions_count: int

    # errors: Optional[List[str]] = None
    facts: List[str] = []


class Scan(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)

    state: ScanState = ScanState.UNKNOWN

    case_id: uuid.UUID
    facts: List[BaseFact] = []
    scan_type: str
    config: ScanConfig

    class Config(BaseConfig):
        extra = "ignore"
        use_enum_values = True
