# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

from celery import group
from loguru import logger
from celery.schedules import schedule

from salver.controller import models
from salver.common.models import ScanState
from salver.controller.app import celery_app, db_manager
from salver.controller.services import agents, scans

@celery_app.task
def ping():
    logger.debug("ping")
    from salver.controller.services.agents_tasks import ping

    return ping()


@celery_app.task
def list_agents():
    a = [
        models.Agent(name=name, collectors=collectors)
        for name, collectors in agents.available_agents.items()
    ]
    return a



@celery_app.task
def reload_agents():
    logger.debug("Reloading agents")
    agents.refresh_agents()


@celery_app.task
def launch_scan(scan_id: UUID):
    print("@@@@@@@@@@@@@@@@@@@", scan_id)
    logger.info(f"Launch scan {scan_id}")
    scan = db_manager.get_scan(scan_id)
    print("!!!!", scan)
    db_manager.update_scan_state(scan.external_id, ScanState.STARTING)
    scan_facts = db_manager.get_input_facts_for_scan(scan_id)
    try:
        r = scans.launch(scan, scan_facts)
    except Exception as err:
        print("ERR LAUNCH", err)
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
