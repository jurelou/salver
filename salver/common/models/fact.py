# -*- coding: utf-8 -*-
import hashlib
from time import time
from typing import Optional

from pydantic import Field, BaseModel, BaseConfig, root_validator


class BaseFact(BaseModel):


    class Config(BaseConfig):
        extra = 'allow'

    # @staticmethod
    # def make_mapping(m):
    #     m['mappings']['properties']['first_seen'] = {'type': 'float'}
    #     m['mappings']['properties']['last_seen'] = {'type': 'float'}
    #     return m

    # @classmethod
    # def elastic_mapping(cls):
    #     return BaseFact.make_mapping({'mappings': {'properties': {}}})
