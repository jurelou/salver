# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from time import time
from typing import List, Optional

from pydantic import Field, BaseModel, BaseConfig

from salver.facts import all_facts
from salver.common.models.fact import BaseFact
from salver.common.models.scan import Scan, ScanState, ScanConfig
from salver.common.database.models.scan import ScanInDB

# class GenericFact(BaseFact):
#     fact_type: str

# class ScanInRequest(Scan):
#     facts: List[GenericFact] = []

#     def json(self, *_):
#         res = self.dict(exclude={"facts", "case_id"})
#         res["case_id"] = self.case_id.hex
#         res["facts"] = [ {
#                 "fact_type": f.fact_type,
#                 "fact": f.json(exclude={"fact_type"})
#             } for f in self.facts]

#         print("JSONNNNNNNNNNNNN", res)
#         return self.__config__.json_dumps(res)

#     @classmethod
#     def parse_obj(cls, obj) -> "ScanInRequest":
#         facts = obj.pop("facts", None)
#         res = cls(**obj)
#         if facts:
#             res.facts = [all_facts[f["fact_type"]].parse_raw(f["fact"]) for f in facts]
#         print("PARSERAWWWWWWWW", res)
#         return res


class ScanInResponse(ScanInDB):
    pass
    # def json(self, *_):
    #     res = self.dict(exclude={"facts", "case_id", "external_id"})
    #     res["case_id"] = self.case_id.hex
    #     res["external_id"] = self.external_id.hex
    #     res["facts"] = [
    #         {"fact": f.json(), "fact_type": f.schema()["title"]} for f in self.facts
    #     ]
    #     return self.__config__.json_dumps(res)
