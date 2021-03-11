import uuid
from time import time
from typing import List

from pydantic import BaseConfig, BaseModel, Field

from opulence.common.fact import BaseFact


class Scan(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)
    scan_type: str

    facts: List[BaseFact] = []
    # collector_name: str

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "allow"
        # json_encoders = {
        #     uuid.UUID: lambda u: u.hex
        # }
