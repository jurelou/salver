# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from time import time
from typing import List, Optional

from pydantic import Field, BaseModel, BaseConfig

from salver.facts import all_facts
from salver.common.models.fact import BaseFact
from salver.common.models.scan import Scan, ScanState, ScanConfig


class ScanInDB(Scan):
    created_on: float = Field(default_factory=time)
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    state: ScanState = ScanState.UNKNOWN
