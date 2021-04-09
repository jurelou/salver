# -*- coding: utf-8 -*-
import json
from uuid import UUID

# from salver.common.models.scan import Scan
from salver.facts import all_facts
from salver.controller import models

# from salver.common.models.case import Case
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
        elif isinstance(obj, models.UUIDResponse):
            return {"__type__": "__uuid_response__", "res": obj.json()}

        elif isinstance(obj, models.ScanInResponse):
            return {
                "__type__": "__scan_res__",
                "scan": obj.json(),
            }
        elif isinstance(obj, models.ScanInRequest):
            return {
                "__type__": "__scan_req__",
                "scan": obj.json(),
            }

        elif isinstance(obj, models.CaseInRequest):
            return {
                "__type__": "__case_req__",
                "case": obj.json(),
            }
        elif isinstance(obj, models.CaseInResponse):
            return {
                "__type__": "__case_res__",
                "case": obj.json(),
            }

        return json.JSONEncoder.default(self, obj)


def decode(obj):

    if "__type__" in obj:
        if obj["__type__"] == "__fact__":
            return all_facts[obj["fact_type"]].parse_raw(obj["fact"])
        elif obj["__type__"] == "__uuid__":
            return UUID(obj["uuid"])
        elif obj["__type__"] == "__uuid_response__":
            return models.UUIDResponse.parse_raw(obj["res"])
        # elif obj["__type__"] == "__scan_result__":
        #    return ScanResult.parse_raw(obj["scan_result"])
        elif obj["__type__"] == "__scan_req__":
            return models.ScanInRequest.parse_raw(obj["scan"])
        elif obj["__type__"] == "__case_req__":
            return models.CaseInRequest.parse_raw(obj["case"])
        elif obj["__type__"] == "__case_res__":
            return models.CaseInResponse.parse_raw(obj["case"])
        elif obj["__type__"] == "__scan_res__":
            return models.ScanInResponse.parse_raw(obj["scan"])
    return obj


def json_dumps(obj):
    return json.dumps(obj, cls=encode)


def json_loads(obj):
    return json.loads(obj, object_hook=decode)
