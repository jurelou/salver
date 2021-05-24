# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel


class Collector(BaseModel):
    name: str
    enabled: bool
    allowed_input: List[str]
    # TODO: collector config, ...
