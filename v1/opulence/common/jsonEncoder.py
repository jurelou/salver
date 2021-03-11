from datetime import datetime
import json
from uuid import UUID

from opulence.facts.bases import BaseFact

from .fields import BaseField
from .job import Result
from .utils import datetime_to_str
from .utils import str_to_datetime


class encode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Result):
            return {"__type__": "__result__", "result": obj.to_json()}
        elif isinstance(obj, BaseFact):
            return {"__type__": "__basefact__", "fact": obj.to_json()}
        elif isinstance(obj, BaseField):
            return {"__type__": "__basefield__", "field": obj.to_json()}
        elif isinstance(obj, datetime):
            return {"__type__": "__datetime__", "epoch": datetime_to_str(obj)}
        elif isinstance(obj, UUID):
            return {"__type__": "__uuid__", "uuid": obj.hex}
        return json.JSONEncoder.default(self, obj)  # pragma: no cover


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__result__":
            return Result.from_json(obj["result"])
        elif obj["__type__"] == "__basefact__":
            return BaseFact.from_json(obj["fact"])
        elif obj["__type__"] == "__basefield__":
            return BaseField.from_json(obj["field"])
        elif obj["__type__"] == "__datetime__":
            return str_to_datetime(obj["epoch"])
        elif obj["__type__"] == "__uuid__":
            return UUID(obj["uuid"])

    return obj


def custom_dumps(obj):
    return json.dumps(obj, cls=encode)


def custom_loads(obj):
    return json.loads(obj, object_hook=decode)
