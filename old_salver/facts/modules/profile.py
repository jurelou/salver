# -*- coding: utf-8 -*-
from salver.common.models.fact import BaseFact


class Profile(BaseFact):
    url: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'url': {'type': 'keyword'}}}},
        )
