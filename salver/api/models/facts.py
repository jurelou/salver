# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, BaseConfig

from salver.common.models import BaseFact


class GenericFact(BaseModel):
    fact_type: str

    class Config(BaseConfig):
        extra = 'allow'


class FactInResponse(GenericFact):
    pass


class FactsInResponse(BaseModel):
    facts: List[FactInResponse]


class FactInRequest(GenericFact):
    fact: BaseFact
