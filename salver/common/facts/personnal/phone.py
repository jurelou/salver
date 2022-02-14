# -*- coding: utf-8 -*-
from salver.common.facts import BaseFact


class Phone(BaseFact):
    number: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'number': {'type': 'keyword'}}}},
        )