from typing import List

from pydantic import BaseModel, BaseConfig

from salver.controller.models import Agent


class FactInResponse(BaseModel):
    fact_type: str

    class Config(BaseConfig):
        extra = "allow"


class FactsInResponse(BaseModel):
    facts: List[FactInResponse]
