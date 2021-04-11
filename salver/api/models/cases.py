from salver.controller.models import Case
from pydantic import BaseModel

from typing import List

class CaseInResponse(BaseModel):
    case: Case

class CasesInResponse(BaseModel):
    cases: List[Case]