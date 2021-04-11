# -*- coding: utf-8 -*-
from fastapi import APIRouter,Request
from salver.api.models.cases import CaseInResponse, CasesInResponse
from salver.api.models.uuid import UUIDsInResponse
from salver.api.services.remote_tasks import sync_call
from fastapi import HTTPException
from salver.controller.services.database.exceptions import CaseNotFound
from uuid import UUID
router = APIRouter()

@router.get("/", response_model=UUIDsInResponse)
async def get_cases():
    cases = sync_call("salver.controller.tasks.list_cases")
    print("!!!!!", cases)
    return UUIDsInResponse(
        ids=[c.id for c in cases]
    )
    # return AgentsInResponse(agents=agents)

@router.get("/{case_id}", response_model=CaseInResponse)
async def get_case(case_id: UUID):
    try:        
        case = sync_call("salver.controller.tasks.get_case", args=[case_id])
        return CaseInResponse(case=case)
    except CaseNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))
