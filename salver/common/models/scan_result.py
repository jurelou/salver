# -*- coding: utf-8 -*-
from typing import List, Optional

from pydantic import BaseModel


class CollectResult(BaseModel):
    duration: float
    executions_count: int

    # errors: Optional[List[str]] = None
    facts: List[str] = []
