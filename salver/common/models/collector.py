# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel


class Collector(BaseModel):
    name: str
    enabled: bool
    # TODO: add allowed facts, collector config, ...

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        return Collector(**obj)
