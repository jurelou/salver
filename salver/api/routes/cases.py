# -*- coding: utf-8 -*-
from fastapi import APIRouter,Request, Depends
# from salver.api.models.cases import CaseInResponse, CasesInResponse

from salver.api.models.cases import CaseInResponse
from salver.api.models.uuid import UUIDsInResponse

from salver.api.services.remote_tasks import sync_call
from fastapi import HTTPException
from salver.common.database.exceptions import CaseNotFound
from uuid import UUID
from salver.common.database import DatabaseManager

from salver.api.services.database import get_database
router = APIRouter()

@router.get("/", response_model=UUIDsInResponse)
async def get_cases(
    db: DatabaseManager = Depends(get_database)
):
    cases_ids = db.list_cases()
    return UUIDsInResponse(
        ids=cases_ids
    )

@router.get("/{case_id}", response_model=CaseInResponse)
async def get_case(
    case_id: UUID,
    db: DatabaseManager = Depends(get_database)
    ):
    try:
        case = db.get_case(case_id)
        scans = db.get_scans_for_case(case_id)
        return CaseInResponse(scans=scans, **case.dict())
    except CaseNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))
