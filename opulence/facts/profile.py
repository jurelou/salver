# -*- coding: utf-8 -*-
from opulence.common.models.fact import BaseFact


class Profile(BaseFact):
    url: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"url": {"type": "keyword"}}}},
        )
