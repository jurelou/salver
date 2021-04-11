# -*- coding: utf-8 -*-
import uuid
from time import time
from typing import List

from pydantic import Field, BaseModel, BaseConfig


class Case(BaseModel):
    name: str