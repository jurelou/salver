# -*- coding: utf-8 -*-
from loguru import logger
from salver.common.kafka import ConsumerCallback
from salver.common.models import Scan
from salver.engine.scans import all_scans
from salver.engine.services import mongodb


ALL_SCANS = {s.name: s for s in all_scans}


class OnScan(ConsumerCallback):
    def __init__(self):
        self.mongo_db = mongodb.get_database()

    def on_message(self, scan:Scan):
        if scan.scan_type not in ALL_SCANS:
            logger.warning(f"Scan {scan.scan_type} does not exists")
            return

        scan_instance = ALL_SCANS[scan.scan_type]()
        scan_instance.configure(scan.config)
        logger.info(f"Launch scan {scan_instance.name}: {scan_instance.external_id}")
        scan_instance.scan(scan.facts)
        logger.info(f"Scan {scan_instance.external_id} finished")

