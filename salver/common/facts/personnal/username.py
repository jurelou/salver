# -*- coding: utf-8 -*-
from salver.common.facts import BaseFact


class Username(BaseFact):
    name: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'name': {'type': 'keyword'}}}},
        )