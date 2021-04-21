# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from salver.api import models
from salver.common.database import DatabaseManager
from salver.common.database import exceptions as db_exceptions
from salver.api.services.database import get_database

router = APIRouter()


@router.get("/", response_model=models.UUIDsInResponse)
async def get_cases(db: DatabaseManager = Depends(get_database)):
    cases_ids = db.list_cases()
    return models.UUIDsInResponse(ids=cases_ids)


@router.get("/{case_id}", response_model=models.CaseInResponse)
async def get_case(case_id: UUID, db: DatabaseManager = Depends(get_database)):
    try:
        case = db.get_case(case_id)
        scans = db.get_scans_for_case(case_id)

        return models.CaseInResponse(
            case=models.CaseResponse(scans=scans, **case.dict())
        )
    except db_exceptions.CaseNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.post("/", response_model=models.UUIDInResponse)
async def create_case(
    case: models.CaseInRequest,
    db: DatabaseManager = Depends(get_database),
):
    try:
        case_id = db.add_case(case)
    except db_exceptions.CaseAlreadyExists as err:
        raise HTTPException(status_code=409, detail=str(err))
    return models.UUIDInResponse(id=case_id)
