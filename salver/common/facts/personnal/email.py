# -*- coding: utf-8 -*-
from salver.common.facts import BaseFact


class Email(BaseFact):
    address: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'address': {'type': 'keyword'}}}},
        )