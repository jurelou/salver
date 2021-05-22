# -*- coding: utf-8 -*-
from pydantic import BaseModel

class Error(BaseModel):
    context: str
    error: str

    class Config:
        extra = 'allow'
