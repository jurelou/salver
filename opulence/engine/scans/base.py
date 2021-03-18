from typing import List
from typing import Optional
import uuid

from pydantic import BaseModel

from opulence.common import models


class BaseScan:
    name: str

    def __init__(self):
        if not self.name:
            raise ValueError(f"{type(self).__name__} should contain a `name` property")

    def configure(self, config: models.ScanConfig):
        pass

    def launch(self, facts):
        print("LAUNCH")
