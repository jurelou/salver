from time import time
from typing import List, Optional
import uuid

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import Field

from opulence.common.models.fact import BaseFact

class   ScanConfig(BaseModel):
    class Config(BaseConfig):
        extra = "allow"

class Scan(BaseModel):
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: float = Field(default_factory=time)
    
    case_id : uuid.UUID
    facts: List[BaseFact] = []
    scan_type: str
    config: ScanConfig

    class Config(BaseConfig):
        extra = "ignore"
