# -*- coding: utf-8 -*-
from pydantic import BaseModel


class Case(BaseModel):
    name: str
