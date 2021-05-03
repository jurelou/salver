# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel, BaseConfig


class BaseFact(BaseModel):
    class Config(BaseConfig):
        extra = 'allow'

    @staticmethod
    def to_dict(obj, *args):
        d = obj.dict()
        d['__fact_type__'] = type(obj).__name__
        return d

    # @staticmethod
    # def make_mapping(m):
    #     m['mappings']['properties']['first_seen'] = {'type': 'float'}
    #     m['mappings']['properties']['last_seen'] = {'type': 'float'}
    #     return m

    # @classmethod
    # def elastic_mapping(cls):
    #     return BaseFact.make_mapping({'mappings': {'properties': {}}})


def facts_to_dict(facts: List[BaseFact]):
    return [BaseFact.to_dict(f) for f in facts]


def facts_from_dict(obj):
    from salver.common.facts import all_facts  # pragma: no cover

    facts = []

    for fact in obj:
        fact_type = fact.pop('__fact_type__', None)
        if fact_type not in all_facts:
            raise ValueError(f'Could get facts from type {fact_type}')
        facts.append(all_facts[fact_type](**fact))
    return facts
