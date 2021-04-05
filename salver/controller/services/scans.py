# -*- coding: utf-8 -*-
from typing import List
from uuid import uuid4

from loguru import logger

from salver.common.models.scan import Scan
from salver.controller.scans.factory import ScanFactory

all_scans = ScanFactory().build()


def schedule():
    # from salver.engine.controllers.periodic_tasks import add_periodic_task
    add_periodic_task(
        app=celery_app, interval=1, task_path="salver.controller.tasks.toto",
    )


def launch(scan: Scan):
    logger.info(f"Launch scan {scan.external_id} of type {scan.scan_type}")

    if scan.scan_type not in all_scans:
        logger.error(f"Scan {scan.scan_type} not found")
        raise ValueError(f"Scan {scan.scan_type} not found")

    scan_class = all_scans[scan.scan_type]()
    scan_class.scan_id = scan.external_id
    scan_class.configure(scan.config)
    scan_class.scan(scan.facts)
