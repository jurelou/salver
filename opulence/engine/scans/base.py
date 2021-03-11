from typing import List
from typing import Optional
import uuid

from pydantic import BaseModel

from opulence.common.fact import BaseFact
from opulence.engine.models.scan import Scan


class BaseScanConfig(BaseModel):
    external_id: uuid.UUID
    facts: List[BaseFact]


class BaseScan:
    name: Optional[str] = None

    def __init__(self):
        if not self.name:
            raise ValueError(f"{type(self).__name__} should contain a `name` property")

    def configure(self, config):
        pass

    def launch(self, facts):
        print("LAUNCH")
