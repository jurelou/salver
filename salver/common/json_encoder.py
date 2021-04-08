# -*- coding: utf-8 -*-
import json
from uuid import UUID

from salver.facts import all_facts
from salver.common.models.fact import BaseFact
from salver.common.models.scan_result import ScanResult


class encode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseFact):
            return {
                "__type__": "__fact__",
                "fact": obj.json(),
                "fact_type": obj.schema()["title"],
            }
        elif isinstance(obj, UUID):
            return {"__type__": "__uuid__", "uuid": obj.hex}
        elif isinstance(obj, ScanResult):
            return {
                "__type__": "__scan_result__",
                "scan_result": obj.json(),
            }

        return json.JSONEncoder.default(self, obj)


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__fact__":
            return all_facts[obj["fact_type"]].parse_raw(obj["fact"])
        elif obj["__type__"] == "__uuid__":
            return UUID(obj["uuid"])
        elif obj["__type__"] == "__scan_result__":
            return ScanResult.parse_raw(obj["scan_result"])
    return obj


def json_dumps(obj):
    return json.dumps(obj, cls=encode)


def json_loads(obj):
    return json.loads(obj, object_hook=decode)
