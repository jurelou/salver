# -*- coding: utf-8 -*-
import uuid
from typing import List

from salver.common.models import Case


class CaseInRequest(Case):
    pass


class CaseInResponse(Case):
    scans: List[uuid.UUID] = []
