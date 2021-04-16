# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from salver.api import models
from salver.facts import all_facts
from salver.common.models import Scan
from salver.common.database import DatabaseManager
from salver.common.database import exceptions as db_exceptions
from salver.api.services.database import get_database
from salver.api.services.remote_tasks import sync_call

router = APIRouter()


@router.get("/", response_model=models.UUIDsInResponse)
async def get_scans(db: DatabaseManager = Depends(get_database)):
    scans_ids = db.list_scans()
    return models.UUIDsInResponse(ids=scans_ids)


@router.get("/{scan_id}")
async def get_scan(scan_id: UUID, db: DatabaseManager = Depends(get_database)):

    try:
        scan_db = db.get_scan(scan_id)
        facts = db.get_input_facts_for_scan(scan_id)
        facts = [
            models.FactInResponse(fact_type=f.schema()["title"], **f.dict())
            for f in facts
        ]
        return models.ScanInResponse(facts=facts, **scan_db.dict())
    except db_exceptions.ScanNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.post("/", response_model=models.UUIDInResponse)
async def create_scan(
    scan_request: models.ScanInRequest, db: DatabaseManager = Depends(get_database),
):
    scan = Scan(**scan_request.dict(exclude={"facts"}))
    facts = [all_facts[f.fact_type](**f.fact.dict()) for f in scan_request.facts]

    try:
        scan_id = db.add_scan(scan)
        db.add_scan_input_facts(scan_id, facts)
    except db_exceptions.CaseNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))
    return models.UUIDInResponse(id=scan_id)
