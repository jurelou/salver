# -*- coding: utf-8 -*-
from pydantic import BaseModel

from salver.common.models import BaseFact


class AgentInfoRequest(BaseModel):
    hello: str = 'world'

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        return AgentInfoRequest(**obj)


class AgentInfo(BaseModel):
    name: str

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        return AgentInfo(**obj)
