# -*- coding: utf-8 -*-
import hashlib
from time import time
from typing import Optional

from pydantic import Field, BaseModel, BaseConfig, root_validator


class BaseFact(BaseModel):
    __hash: Optional[str] = None

    first_seen: float = Field(default_factory=time)
    last_seen: float = Field(default_factory=time)

    def __iter__(self):
        raise TypeError

    @root_validator
    def set_hash(cls, values):
        values.pop("hash__", None)
        m = hashlib.sha256()
        print("!!!!!!!", cls, type(cls))
        if not "required" in cls.schema():
            print(f"Strange fact ..... {cls.schema()}, {cls}, {type(cls)}")
        required_fields = cls.schema()["required"]

        for k in sorted(values):
            if k in required_fields:
                m.update(str(k).encode() + str(values[k]).encode())
        values["hash__"] = m.hexdigest()
        return values

    class Config(BaseConfig):
        extra = "allow"

    @staticmethod
    def make_mapping(m):
        m["mappings"]["properties"]["first_seen"] = {"type": "float"}
        m["mappings"]["properties"]["last_seen"] = {"type": "float"}
        return m

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping({"mappings": {"properties": {}}})

    @staticmethod
    def from_obj(fact_type: str, data):
        from salver.facts import all_facts  # pragma: nocover

        return all_facts[fact_type](**data)
