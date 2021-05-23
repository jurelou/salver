# -*- coding: utf-8 -*-
from pydantic import BaseModel

class Error(BaseModel):
    context: str
    error: str

    class Config:
        extra = 'allow'

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        return Error(**obj)