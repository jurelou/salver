from salver.controller.models import Agent
from pydantic import BaseModel, BaseConfig

from typing import List

class FactInResponse(BaseModel):
    fact_type: str

    class Config(BaseConfig):
        extra = "allow"

class FactsInResponse(BaseModel):
    facts: List[FactInResponse]
