# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from typing import List

from pydantic import Field, BaseModel, BaseConfig

from salver.common.fact import BaseFact


class ScanRequest(BaseModel):
    facts: List[BaseFact]
    identifier: uuid.UUID = Field(default_factory=uuid.uuid4)


# class ScanConfig(BaseModel):
#     class Config:
#         extra = 'allow'

# class ScanState(str, Enum):
#     UNKNOWN = 'unknown'
#     CREATED = 'created'
#     STARTING = 'starting'
#     STARTED = 'started'
#     FINISHED = 'finished'
#     ERRORED = 'errored'


# class Scan(BaseModel):
#     scan_type: str
#     config: ScanConfig

#     facts: List[BaseFact]

#     state: ScanState = ScanState.UNKNOWN

#     external_id: uuid.UUID = Field(default_factory=uuid.uuid4)

#     class Config:
#         extra = 'ignore'
#         use_enum_values = True

#     @staticmethod
#     def to_dict(obj, *args):
#         # d = obj.dict(exclude={'facts', 'external_id'})
#         d = obj.dict(exclude={'facts', 'external_id'})
#         d['facts'] = facts_to_dict(obj.facts)
#         d['external_id'] = obj.external_id.hex
#         return d

#     @staticmethod
#     def from_dict(obj, _):
#         facts = obj.pop('facts', [])
#         return Scan(facts=facts_from_dict(facts), **obj)
