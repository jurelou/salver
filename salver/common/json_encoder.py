import json
from datetime import datetime
from uuid import UUID

from salver.common.utils import datetime_to_str, str_to_datetime
from salver.common.facts import BaseFact, all_facts


class encode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseFact):
            return {
                "__type__": "__fact__",
                "__fact_type__": obj.schema()["title"],
                "fact": obj.json(),
            }
        elif isinstance(obj, datetime):
            return {"__type__": "__datetime__", "epoch": datetime_to_str(obj)}
        elif isinstance(obj, UUID):
            return {"__type__": "__uuid__", "uuid": obj.hex}
        
        return json.JSONEncoder.default(self, obj)  # pragma: no cover


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__fact__":
            return all_facts[obj["__fact_type__"]].parse_raw(obj["fact"])
        elif obj["__type__"] == "__datetime__":
            return str_to_datetime(obj["epoch"])
        elif obj["__type__"] == "__uuid__":
            return UUID(obj["uuid"])
    return obj


def custom_dumps(obj):
    return json.dumps(obj, cls=encode)


def custom_loads(obj):
    return json.loads(obj, object_hook=decode)