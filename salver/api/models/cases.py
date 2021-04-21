# -*- coding: utf-8 -*-
import uuid
from typing import List

from pydantic import BaseModel

from salver.common.models import Case


class CaseInRequest(Case):
    pass


class CaseResponse(Case):
    scans: List[uuid.UUID] = []


class CaseInResponse(BaseModel):
    case: CaseResponse
