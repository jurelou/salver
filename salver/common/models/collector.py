# -*- coding: utf-8 -*-
from typing import List, Optional

from pydantic import BaseModel

from salver.common.limiter import RequestRate


class CollectorBaseConfig(BaseModel):
    name: str
    limiter: Optional[List[RequestRate]]

    # periodic: bool = False
    # schedule: Optional[Schedule] = None

    # @root_validator
    # def check_schedule(cls, values):
    #     is_periodic = values.get('periodic')
    #     if is_periodic:
    #         if not values.get('schedule'):
    #             raise ValueError(f'Schedule should be set for collector {values.get("name")}')
    #     return values

    class Config:
        use_enum_values = True
        json_encoders = {RequestRate: lambda v: str(v)}


class Collector(BaseModel):
    active: bool
    name: str
    config: Optional[CollectorBaseConfig] = None
    input_facts: Optional[List[str]] = None
