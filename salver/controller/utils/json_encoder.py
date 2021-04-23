# -*- coding: utf-8 -*-
import json

from salver.controller.models import Agent
from salver.common.models.fact import BaseFact
from salver.common.json_encoder import decode, encode_map

encode_map.update(
    {
        Agent.__module__: {
            'type': '__agent__',
            'to_json': lambda obj: {
                '__salver_type__': '__agent__',
                'agent': obj.json(),
            },
            'from_json': lambda obj: Agent.parse_raw(obj['agent']),
        },
    },
)


class encode(json.JSONEncoder):  # pragma: no cover
    def default(self, obj):
        if not hasattr(obj, '__module__'):
            return json.JSONEncoder.default(self, obj)
        if isinstance(obj, BaseFact):
            return {
                '__salver_type__': '__fact__',
                'fact': obj.json(),
                'fact_type': obj.schema()['title'],
            }
        mod = obj.__module__
        if mod not in encode_map.keys():
            return json.JSONEncoder.default(self, obj)
        return encode_map[mod]['to_json'](obj)


def json_dumps(obj):
    return json.dumps(obj, cls=encode)


def json_loads(obj):
    return json.loads(obj, object_hook=decode)
