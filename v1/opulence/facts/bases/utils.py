# -*- coding: utf-8 -*-
from opulence.common.patterns import is_composite

from .baseFact import BaseFact


def is_fact_or_composite(obj):
    return is_composite(obj) or isinstance(obj, BaseFact)


def is_fact(obj):
    return isinstance(obj, BaseFact)
