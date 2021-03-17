# -*- coding: utf-8 -*-
from opulence.common.models.fact import BaseFact


class Email(BaseFact):
    address: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {"mappings": {"properties": {"address": {"type": "keyword"}}}},
        )
