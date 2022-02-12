# -*- coding: utf-8 -*-
import hashlib
from typing import List
from uuid import UUID

from pydantic import BaseModel, BaseConfig, root_validator


class BaseFact(BaseModel):
    __hash__: str = ''

    class Config(BaseConfig):
        extra = 'allow'

    @root_validator
    def set_hash(cls, values):
        if 'required' not in cls.schema():
            return values
        values.pop('__hash__', None)
        m = hashlib.sha256()
        required_fields = cls.schema()['required']
        for k in sorted(values):
            if k in required_fields:
                m.update(str(k).encode() + str(values[k]).encode())
        values['__hash__'] = m.hexdigest()
        return values

    @staticmethod
    def to_dict(obj, *args):
        d = obj.dict()
        d['__fact_type__'] = type(obj).__name__
        return d
