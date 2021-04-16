# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel

from salver.common.models import Scan, BaseFact
from salver.common.database.models.scan import ScanInDB

from .facts import FactInResponse

# from salver.controller.models import ScanInRequest as ControlerScanInRequest


class GenericFact(BaseModel):
    fact_type: str
    fact: BaseFact


class ScanInRequest(Scan):
    facts: List[GenericFact] = []

    class Config:
        schema_extra = {
            "example": {
                "case_id": "4242",
                "facts": [
                    {
                        "fact_type": "Person",
                        "fact": {"firstname": "John", "lastname": "Doe", "age": 42},
                    },
                ],
                "scan_type": "single_collector",
                "config": {"collector_name": "dummy-docker-collector"},
            },
        }


class ScanInResponse(ScanInDB):
    facts: List[FactInResponse]
