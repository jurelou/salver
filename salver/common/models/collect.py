# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from typing import List

from pydantic import Field, BaseModel, BaseConfig

from .fact import BaseFact, facts_to_dict, facts_from_dict


class CollectState(str, Enum):
    UNKNOWN = 'unknown'
    CREATED = 'created'

    STARTING = 'starting'
    STARTED = 'started'
    FINISHED = 'finished'
    ERRORED = 'errored'


class Collect(BaseModel):
    state: CollectState = CollectState.UNKNOWN
    collector_name: str
    facts: List[BaseFact]
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        extra = 'ignore'
        use_enum_values = True

    @staticmethod
    def to_dict(obj, _):
        d = obj.dict(exclude={'facts', 'external_id'})
        d['facts'] = facts_to_dict(obj.facts)
        d['external_id'] = obj.external_id.hex
        return d

    @staticmethod
    def from_dict(obj, _):
        facts = obj.pop('facts', [])
        return Collect(facts=facts_from_dict(facts), **obj)
