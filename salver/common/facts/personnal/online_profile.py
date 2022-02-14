# -*- coding: utf-8 -*-
from salver.common.facts import BaseFact


class OnlineProfile(BaseFact):
    url: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'url': {'type': 'keyword'}}}},
        )