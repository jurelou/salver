# -*- coding: utf-8 -*-
from typing import List
from loguru import logger

from salver.common.facts import BaseFact
from salver.engine.scans import ScanStrategy


class FullScanStrategy(ScanStrategy):

    def run(self, facts: List[BaseFact]):
        scan_id = self.run_agent_scan(facts=facts)
        logger.info(f"Launched full scan: {scan_id}")