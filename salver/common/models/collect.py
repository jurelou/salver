# -*- coding: utf-8 -*-
from pydantic import BaseModel
from salver.common.models import BaseFact
from typing import List, Union
from salver.common.avro import make_serializer, make_deserializer


class CollectRequest(BaseModel):
    collector_name: str = "mdr"
    facts: List[Union[str, int]]


    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        return CollectRequest(**obj)
