# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel



class CollectorBaseConfig(BaseModel):
    name: str
    enabled: bool
    # TODO: add allowed facts, collector config, ...

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    class Config:
        use_enum_values = True
        json_encoders = {RequestRate: lambda v: str(v)}


class Collector(BaseModel):
    active: bool
    name: str
    config: Optional[CollectorBaseConfig] = None
    input_facts: Optional[List[str]] = None
