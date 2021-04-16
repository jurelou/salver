from typing import List

from pydantic import BaseModel, BaseConfig

from salver.controller.models import Agent


class GenericFact(BaseModel):
    fact_type: str

    class Config(BaseConfig):
        extra = "allow"


class FactInResponse(GenericFact):
    pass


class FactsInResponse(BaseModel):
    facts: List[FactInResponse]


class FactInRequest(GenericFact):
    pass
