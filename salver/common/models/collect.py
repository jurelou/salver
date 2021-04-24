# -*- coding: utf-8 -*-
from pydantic import BaseModel
from salver.common.models import BaseFact
from typing import List, Union
from salver.common.avro import make_serializer, make_deserializer
from salver.common.facts import all_facts

class CollectRequest(BaseModel):
    collector_name: str
    facts: List[BaseFact]

    @staticmethod
    def to_dict(obj, _):
        return obj.dict()

    @staticmethod
    def from_dict(obj, _):
        facts = []
        obj_facts = obj.pop("facts", [])
        for fact in obj_facts:
            fact_type = fact.pop("__fact_type__")
            if fact_type not in all_facts:
                raise ValueError(f"Could not deserialize fact of type {fact_type}")
            facts.append(all_facts[fact_type](**fact))
        return CollectRequest(facts=facts, **obj)
