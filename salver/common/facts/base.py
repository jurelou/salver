# -*- coding: utf-8 -*-
import hashlib
from uuid import UUID
from typing import List

from pydantic import BaseModel, BaseConfig, root_validator


class BaseFact(BaseModel):
    fact_hash: str = ""

    class Config(BaseConfig):
        extra = "allow"

    @root_validator
    def set_hash(cls, values):
        if "required" not in cls.schema():
            return values
        values.pop("fact_hash", None)
        m = hashlib.sha256()
        required_fields = cls.schema()["required"]
        for k in sorted(values):
            if k in required_fields:
                m.update(str(k).encode() + str(values[k]).encode())
        values["fact_hash"] = m.hexdigest()
        return values

    @staticmethod
    def to_dict(obj, *args):
        d = obj.dict()
        d["__fact_type__"] = type(obj).__name__
        return d

    @staticmethod
    def make_mapping(m):
        m['mappings']['properties']['fact_type'] = {'type': 'keyword'}
        m['mappings']['properties']['fact_source'] = {'type': 'keyword'}
        m['mappings']['properties']['fact_hash'] = {'type': 'keyword'}
        m['mappings']['properties']['scan_id'] = {'type': 'keyword'}

        return m