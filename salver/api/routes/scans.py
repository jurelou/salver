# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import Depends, Request, APIRouter, HTTPException

from salver.api.models.uuid import UUIDsInResponse
from salver.common.database import DatabaseManager
from salver.api.models.facts import FactInResponse
from salver.api.models.scans import ScanInResponse
from salver.api.services.database import get_database
from salver.api.services.remote_tasks import sync_call
from salver.common.database.exceptions import ScanNotFound

router = APIRouter()


@router.get("/", response_model=UUIDsInResponse)
async def get_scans(db: DatabaseManager = Depends(get_database)):
    scans_ids = db.list_scans()
    return UUIDsInResponse(ids=scans_ids)


@router.get("/{scan_id}")
async def get_scan(scan_id: UUID, db: DatabaseManager = Depends(get_database)):

    try:
        scan_db = db.get_scan(scan_id)
        facts = db.get_input_facts_for_scan(scan_id)
        facts = [
            FactInResponse(fact_type=f.schema()["title"], **f.dict()) for f in facts
        ]
        return ScanInResponse(facts=facts, **scan_db.dict())
    except ScanNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))
