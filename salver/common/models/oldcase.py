# -*- coding: utf-8 -*-
import uuid
from time import time

from pydantic import Field, BaseModel, BaseConfig


class Case(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)

    name: str

    class Config(BaseConfig):
        extra = "ignore"
        # json_encoders = {
        #     uuid.UUID: lambda u: u.hex
        # }
