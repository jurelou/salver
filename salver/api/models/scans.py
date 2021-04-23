# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel

from salver.common.models import Scan
from salver.common.database.models.scan import ScanInDB

from .facts import FactInRequest, FactInResponse

# from salver.controller.models import ScanInRequest as ControlerScanInRequest


class ScanInRequest(Scan):
    facts: List[FactInRequest] = []

    class Config:
        schema_extra = {
            'example': {
                'case_id': '4242',
                'facts': [
                    {
                        'fact_type': 'Person',
                        'fact': {'firstname': 'John', 'lastname': 'Doe', 'age': 42},
                    },
                ],
                'scan_type': 'single_collector',
                'config': {'collector_name': 'dummy-docker-collector'},
            },
        }


class ScanInResponse(ScanInDB):
    facts: List[FactInResponse]
