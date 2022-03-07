# -*- coding: utf-8 -*-
from typing import List
from loguru import logger

from salver.common.facts import BaseFact
from salver.engine.scans import ScanStrategy


class SingleCollectorStrategy(ScanStrategy):
    def __init__(self, collector_name: str):
        self._collector_name = collector_name

    def run(self, facts: List[BaseFact]):
        scan_id = self.run_agent_scan(collector_name=self._collector_name, facts=facts)
        logger.info(f"Launched single collector ({self._collector_name}) scan: {scan_id}")
