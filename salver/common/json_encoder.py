# -*- coding: utf-8 -*-
import json
from uuid import UUID

from salver.facts import all_facts
from salver.common.models import BaseFact, Collector, ScanResult

encode_map = {
    BaseFact.__module__: {
        'type': '__fact__',
        'to_json': lambda obj: {
            '__salver_type__': '__fact__',
            'fact': obj.json(),
            'fact_type': obj.schema()['title'],
        },
        'from_json': lambda obj: all_facts[obj['fact_type']].parse_raw(obj['fact']),
    },
    UUID.__module__: {
        'type': '__uuid__',
        'to_json': lambda obj: {'__salver_type__': '__uuid__', 'uuid': obj.hex},
        'from_json': lambda obj: UUID(obj['uuid']),
    },
    ScanResult.__module__: {
        'type': '__scan_result__',
        'to_json': lambda obj: {
            '__salver_type__': '__scan_result__',
            'scan_result': obj.json(),
        },
        'from_json': lambda obj: ScanResult.parse_raw(obj['scan_result']),
    },
    Collector.__module__: {
        'type': '__collector__',
        'to_json': lambda obj: {
            '__salver_type__': '__collector__',
            'collector': obj.json(),
        },
        'from_json': lambda obj: Collector.parse_raw(obj['collector']),
    },
}


class encode(json.JSONEncoder):
    def default(self, obj):
        if not hasattr(obj, '__module__'):
            return json.JSONEncoder.default(self, obj)
        mod = obj.__module__
        if mod not in encode_map.keys():
            return json.JSONEncoder.default(self, obj)
        return encode_map[mod]['to_json'](obj)


def decode(obj):
    if '__salver_type__' not in obj:
        return obj
    obj_type = obj['__salver_type__']
    for item in encode_map.values():
        if obj_type == item['type']:
            return item['from_json'](obj)
    print(f'@@@ERROR json decode {type(obj)}: {obj}')
    return obj


def json_dumps(obj):
    return json.dumps(obj, cls=encode)


def json_loads(obj):
    return json.loads(obj, object_hook=decode)
