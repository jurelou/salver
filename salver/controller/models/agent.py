# -*- coding: utf-8 -*-
from typing import List

from pydantic import Field, BaseModel, BaseConfig
from salver.common.models import Collector

class Agent(BaseModel):
    name: str
    collectors: List[Collector]