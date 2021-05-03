# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel

from .collector import Collector


class AgentInfo(BaseModel):
    name: str
    collectors: List[Collector]

    @staticmethod
    def to_dict(obj, _):
        res = obj.dict(exclude={'collectors'})
        res['collectors'] = [c.dict() for c in obj.collectors]
        return res

    @staticmethod
    def from_dict(obj, _):
        return AgentInfo(**obj)
