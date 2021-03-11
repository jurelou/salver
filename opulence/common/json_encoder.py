import json
from uuid import UUID

from opulence.common.fact import BaseFact
from opulence.engine.models.case import Case
from opulence.engine.models.scan import Scan
from opulence.facts import all_facts


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
        elif isinstance(obj, Scan):
            return {
                "__type__": "__scan__",
                "scan": obj.json(),
            }
        elif isinstance(obj, Case):
            return {
                "__type__": "__case__",
                "case": obj.json(),
            }

        return json.JSONEncoder.default(self, obj)


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__fact__":
            return all_facts[obj["fact_type"]].parse_raw(obj["fact"])
        elif obj["__type__"] == "__uuid__":
            return UUID(obj["uuid"])
        elif obj["__type__"] == "__scan__":
            return Scan.parse_raw(obj["scan"])
        elif obj["__type__"] == "__case__":
            return Case.parse_raw(obj["case"])
    return obj


def json_dumps(obj):
    return json.dumps(obj, cls=encode)


def json_loads(obj):
    return json.loads(obj, object_hook=decode)
