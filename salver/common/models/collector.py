# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel


class Collector(BaseModel):
    name: str
    enabled: bool
    # TODO: add allowed facts, collector config, ...
