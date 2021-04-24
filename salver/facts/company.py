# -*- coding: utf-8 -*-
from salver.common.models.fact import BaseFact


class Company(BaseFact):
    naazeme: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'name': {'type': 'keyword'}}}},
        )
