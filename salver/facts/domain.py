# -*- coding: utf-8 -*-
from salver.common.models.fact import BaseFact


class Domain(BaseFact):
    fqdn: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {'mappings': {'properties': {'fqdn': {'type': 'keyword'}}}},
        )
