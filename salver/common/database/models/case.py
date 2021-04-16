# -*- coding: utf-8 -*-
import uuid
from time import time
from typing import List

from pydantic import Field, BaseModel, BaseConfig

from salver.common.models.case import Case


class CaseInDB(Case):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_on: float = Field(default_factory=time)
