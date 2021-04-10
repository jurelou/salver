# -*- coding: utf-8 -*-
import json

from salver.controller import models
from salver.common.models.fact import BaseFact
from salver.common.json_encoder import decode, encode_map

encode_map.update(
    {
        models.UUIDResponse.__module__: {
            "type": "__uuid_response__",
            "to_json": lambda obj: {
                "__salver_type__": "__uuid_response__",
                "res": obj.json(),
            },
            "from_json": lambda obj: models.UUIDResponse.parse_raw(obj["res"]),
        },
        models.ScanInRequest.__module__: {
            "type": "__scan_req__",
            "to_json": lambda obj: {
                "__salver_type__": "__scan_req__",
                "scan": obj.json(),
            },
            "from_json": lambda obj: models.ScanInRequest.parse_raw(obj["scan"]),
        },
        models.CaseInRequest.__module__: {
            "type": "__case_req__",
            "to_json": lambda obj: {
                "__salver_type__": "__case_req__",
                "case": obj.json(),
            },
            "from_json": lambda obj: models.CaseInRequest.parse_raw(obj["case"]),
        },
        models.CaseInResponse.__module__: {
            "type": "__case_res__",
            "to_json": lambda obj: {
                "__salver_type__": "__case_res__",
                "case": obj.json(),
            },
            "from_json": lambda obj: models.CaseInResponse.parse_raw(obj["case"]),
        },
        models.Agent.__module__: {
            "type": "__agent__",
            "to_json": lambda obj: {
                "__salver_type__": "__agent__",
                "agent": obj.json(),
            },
            "from_json": lambda obj: models.Agent.parse_raw(obj["agent"]),
        },
    }
)


class encode(json.JSONEncoder):
    def default(self, obj):
        if not hasattr(obj, "__module__"):
            return json.JSONEncoder.default(self, obj)
        if isinstance(obj, BaseFact):
            return {
                "__salver_type__": "__fact__",
                "fact": obj.json(),
                "fact_type": obj.schema()["title"],
            }
        mod = obj.__module__
        if mod not in encode_map.keys():
            return json.JSONEncoder.default(self, obj)
        return encode_map[mod]["to_json"](obj)


def json_dumps(obj):
    return json.dumps(obj, cls=encode)


def json_loads(obj):
    return json.loads(obj, object_hook=decode)
