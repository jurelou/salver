# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from time import time
from typing import List, Optional

from pydantic import Field, BaseModel, BaseConfig

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
