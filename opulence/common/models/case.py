# -*- coding: utf-8 -*-
from time import time
import uuid

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import Field


class Case(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)

    name: str

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "ignore"
        # json_encoders = {
        #     uuid.UUID: lambda u: u.hex
        # }
