# -*- coding: utf-8 -*-
from celery.schedules import schedule
from loguru import logger

from uuid import UUID
from opulence.common import models
from opulence.engine.app import celery_app
from opulence.engine.controllers import agents_tasks
from opulence.engine.controllers import agents as agents_ctrl
from opulence.engine.controllers import scans as scans_ctrl
from opulence.engine.app import db_manager


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
