# -*- coding: utf-8 -*-

from pydantic import BaseModel

from salver.common.models import BaseFact


class PingRequest(BaseModel):
    ping: str

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        return PingRequest(**obj)
