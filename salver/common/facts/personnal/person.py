# -*- coding: utf-8 -*-
from salver.common.facts import BaseFact


class Person(BaseFact):
    lastname: str
    firstname: str

    @classmethod
    def elastic_mapping(cls):
        return BaseFact.make_mapping(
            {
                'mappings': {
                    'properties': {
                        'lastname': {'type': 'keyword'},
                        'firstname': {'type': 'keyword'},
                    },
                },
            },
        )