# -*- coding: utf-8 -*-
from salver.common.models.fact import BaseFact


class Socket(BaseFact):
    port_number: int
    proto: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {
                "mappings": {
                    "properties": {
                        "port": {"type": "integer"},
                        "proto": {"type": "keyword"},
                    },
                },
            },
        )
