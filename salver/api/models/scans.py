# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from time import time
from typing import List, Optional

from pydantic import Field, BaseModel, BaseConfig

from salver.facts import all_facts
from salver.common.models.scan import Scan, ScanState, ScanConfig
from salver.common.database.models.scan import ScanInDB

from .facts import FactInResponse

# class ScanInRequest(Scan):
#     facts: List[BaseFact] = []

#     def json(self, *_):
#         res = self.dict(exclude={"facts", "case_id"})
#         res["case_id"] = self.case_id.hex
#         res["facts"] = [
#             {"fact": f.json(), "fact_type": f.schema()["title"]} for f in self.facts
#         ]
#         return self.__config__.json_dumps(res)

#     @classmethod
#     def parse_obj(cls, obj) -> "Model":
#         facts = [
#             all_facts[f["fact_type"]].parse_raw(f["fact"]) for f in obj.pop("facts")
#         ]
#         return cls(facts=facts, **obj)


class ScanInResponse(ScanInDB):
    facts: List[FactInResponse]
    # def json(self, *_):
    #     res = self.dict(exclude={"facts", "case_id", "external_id"})
    #     res["case_id"] = self.case_id.hex
    #     res["external_id"] = self.external_id.hex
    #     res["facts"] = [
    #         {"fact": f.json(), "fact_type": f.schema()["title"]} for f in self.facts
    #     ]
    #     return self.__config__.json_dumps(res)
