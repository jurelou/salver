# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from typing import List

from pydantic import Field, BaseModel, BaseConfig

from .fact import BaseFact, facts_to_dict, facts_from_dict


class CollectState(str, Enum):
    UNKNOWN = "unknown"
    CREATED = "created"

    STARTING = "starting"
    STARTED = "started"
    FINISHED = "finished"
    ERRORED = "errored"


class CollectDone(BaseModel):
    collect_id: uuid.UUID
    duration: float
    facts_count: int
    state: CollectState = CollectState.FINISHED

    class Config:
        use_enum_values = True

    @staticmethod
    def to_dict(obj, *args):
        d = obj.dict(exclude={"collect_id"})
        d["collect_id"] = obj.collect_id.hex
        return d

    @staticmethod
    def from_dict(obj, _):
        return CollectDone(**obj)


class CollectResponse(BaseModel):
    fact: BaseFact
    collect_id: uuid.UUID
    scan_id: uuid.UUID
    collector_name: str = "a faire"

    @staticmethod
    def to_dict(obj, *args):
        d = obj.dict(exclude={"fact", "collect_id", "scan_id"})
        d["fact"] = BaseFact.to_dict(obj.fact)
        d["collect_id"] = obj.collect_id.hex
        d["scan_id"] = obj.scan_id.hex
        return d

    @staticmethod
    def from_dict(obj, _):
        fact = obj.pop("fact", None)
        return CollectResponse(fact=facts_from_dict([fact])[0], **obj)


class Collect(BaseModel):
    state: CollectState = CollectState.UNKNOWN
    collector_name: str
    facts: List[BaseFact]
    scan_id: uuid.UUID
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        extra = "ignore"
        use_enum_values = True

    @staticmethod
    def to_dict(obj, *args):
        d = obj.dict(exclude={"facts", "external_id", "scan_id"})
        d["facts"] = facts_to_dict(obj.facts)
        d["external_id"] = obj.external_id.hex
        d["scan_id"] = obj.scan_id.hex
        return d

    @staticmethod
    def from_dict(obj, _):
        facts = obj.pop("facts", [])
        return Collect(facts=facts_from_dict(facts), **obj)
