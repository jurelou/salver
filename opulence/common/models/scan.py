from time import time
from typing import List
import uuid

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import Field

from opulence.common.models.fact import BaseFact


class Scan(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)
    
    case_id : uuid.UUID
    scan_type: str
    facts: List[BaseFact] = []
    # collector_name: str

    class Config(BaseConfig):
        allow_population_by_alias = True
        extra = "ignore"
        # json_encoders = {
        #     uuid.UUID: lambda u: u.hex
        # }
