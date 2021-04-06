# -*- coding: utf-8 -*-
from celery.schedules import schedule
from loguru import logger

from uuid import UUID
from salver.common import models
from salver.controller.app import celery_app
from salver.controller.services import agents_tasks
from salver.controller.services import agents as agents_ctrl
from salver.controller.services import scans as scans_ctrl
from salver.controller.app import db_manager
from celery import group



@celery_app.task
def ping(trail=True):
    logger.debug("ping")
    from salver.controller.services.agents_tasks import ping
    return ping()

@celery_app.task
def reload_agents():
    logger.debug("Reloading agents")
    agents_ctrl.refresh_agents()


@celery_app.task
def launch_scan(scan_id: UUID):
    logger.info(f"Launch scan {scan_id}")
    scan = db_manager.get_scan(scan_id)
    db_manager.update_scan_state(scan.external_id, models.ScanState.STARTING)
    scans_ctrl.launch(scan)

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
