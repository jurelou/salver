# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from time import time
from typing import List, Optional

from pydantic import Field, BaseModel, BaseConfig

from salver.facts import all_facts
from salver.common.models.fact import BaseFact


class ScanState(str, Enum):
    UNKNOWN = "unknown"
    CREATED = "created"

    STARTING = "starting"
    STARTED = "started"
    FINISHED = "finished"
    ERRORED = "errored"


class ScanConfig(BaseModel):
    class Config(BaseConfig):
        extra = "allow"


class Scan(BaseModel):
    case_id: uuid.UUID
    scan_type: str
    config: ScanConfig

    class Config:
        extra = "ignore"
        use_enum_values = True


class ScanInRequest(Scan):
    facts: List[BaseFact] = []

    def json(self, *_):
        res = self.dict(exclude={"facts", "case_id"})
        res["case_id"] = self.case_id.hex
        res["facts"] = [
            {"fact": f.json(), "fact_type": f.schema()["title"]} for f in self.facts
        ]
        return self.__config__.json_dumps(res)

    @classmethod
    def parse_obj(cls, obj) -> "Model":
        facts = [
            all_facts[f["fact_type"]].parse_raw(f["fact"]) for f in obj.pop("facts")
        ]
        return cls(facts=facts, **obj)


class ScanInDB(Scan):
    created_on: float = Field(default_factory=time)
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    state: ScanState = ScanState.UNKNOWN

class ScanInResponse(ScanInDB, ScanInRequest):
    def json(self, *_):
        res = self.dict(exclude={"facts", "case_id", "external_id"})
        res["case_id"] = self.case_id.hex
        res["external_id"] = self.external_id.hex
        res["facts"] = [
            {"fact": f.json(), "fact_type": f.schema()["title"]} for f in self.facts
        ]
        return self.__config__.json_dumps(res)
