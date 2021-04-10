# -*- coding: utf-8 -*-
from typing import List, Optional

from pydantic import BaseModel


class Collector(BaseModel):
    name: str
    executions_count: int

    # errors: Optional[List[str]] = None
    facts: List[str] = []
