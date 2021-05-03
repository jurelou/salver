# -*- coding: utf-8 -*-
from typing import List

from salver.common.models import Collect, BaseFact


class FactInDB(BaseFact):
    __fact_type__: str


class CollectInDB(Collect):
    facts: List[FactInDB]
