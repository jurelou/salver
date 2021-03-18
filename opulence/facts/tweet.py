# -*- coding: utf-8 -*-
from opulence.common.models.fact import BaseFact


class Tweet(BaseFact):
    content: str
    id: str
    date: str
    rt: bool

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {
                "mappings": {
                    "properties": {
                        "content": {"type": "text"},
                        "id": {"type": "keyword"},
                        "date": {"type": "text"},
                        "rt": {"type": "boolean"},
                    },
                },
            },
        )
