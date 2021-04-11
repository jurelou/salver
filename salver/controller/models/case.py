# -*- coding: utf-8 -*-
import uuid
from time import time
from typing import List

from pydantic import Field, BaseModel, BaseConfig

from salver.common.models import Case


class CaseInRequest(Case):
    pass


class CaseInResponse(Case):
    scans: List[uuid.UUID] = []
