# -*- coding: utf-8 -*-
import uuid
from time import time

from pydantic import Field

from salver.common.models.scan import Scan, ScanState


class ScanInDB(Scan):
    created_on: float = Field(default_factory=time)
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    state: ScanState = ScanState.UNKNOWN
