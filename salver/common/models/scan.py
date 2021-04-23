# -*- coding: utf-8 -*-
import uuid
from enum import Enum

from pydantic import BaseModel, BaseConfig


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
    scan_type: str
    config: ScanConfig

    class Config:
        extra = "ignore"
        use_enum_values = True
