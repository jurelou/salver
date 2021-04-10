# -*- coding: utf-8 -*-
from uuid import UUID

from celery import group
from loguru import logger
from celery.schedules import schedule

from salver.controller import models
from salver.controller.app import celery_app, db_manager
from salver.controller.services import scans as scans_ctrl
from salver.controller.services import agents as agents_ctrl
from salver.controller.services import agents_tasks


@celery_app.task
def ping():
    logger.debug("ping")
    from salver.controller.services.agents_tasks import ping

    return ping()


@celery_app.task
def list_collectors():
    from salver.controller.services.agents import available_agents
    print("!!!!!", available_agents)
    # return ping()


@celery_app.task
def get_case(case_id: UUID) -> models.CaseInResponse:
    case_db = db_manager.get_case(case_id)
    scans = db_manager.get_scans_for_case(case_id)
    return models.CaseInResponse(scans=scans, **case_db.dict())


@celery_app.task
def get_scan(scan_id: UUID) -> models.ScanInResponse:
    scan_db = db_manager.get_scan(scan_id)
    facts = db_manager.get_input_facts_for_scan(scan_id)

    return models.ScanInResponse(
        facts=facts,
        **scan_db.dict(),
    )


@celery_app.task
def create_case(case: models.CaseInRequest) -> models.UUIDResponse:
    case_id = db_manager.add_case(case)
    print("CREATE CASE")
    return models.UUIDResponse(id=case_id)


@celery_app.task
def create_scan(scan: models.ScanInRequest) -> models.UUIDResponse:
    scan_id = db_manager.add_scan(scan)
    print("CREATE SCAN")
    return models.UUIDResponse(id=scan_id)


@celery_app.task
def reload_agents():

    logger.debug("Reloading agents")
    agents_ctrl.refresh_agents()


# @celery_app.task
# def create_scan(scan: models.ScanInRequest):
#     pass


@celery_app.task
def launch_scan(scan_id: UUID):
    logger.info(f"Launch scan {scan_id}")
    scan = db_manager.get_scan(scan_id)
    db_manager.update_scan_state(scan.external_id, models.ScanState.STARTING)
    scan_facts = db_manager.get_input_facts_for_scan(scan_id)
    print("))))))))", scan_facts)
    r = scans_ctrl.launch(scan, scan_facts)
    print("LAUNCH RES", r)
    return "result ok"
    # try:
    #     scan = scan_ctrl.get(scan_id)
    #     scan_ctrl.launch(scan)

    # except Exception as err:
    #     import sys
    #     import traceback

    #     traceback.print_exc(file=sys.stdout)
    #     logger.critical(err)

    # scan_ctrl.create(scan)
    # case_ctrl.add_scan(case_id, scan.external_id)
