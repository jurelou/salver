# -*- coding: utf-8 -*-
from typing import List

from loguru import logger

from salver.common.facts import BaseFact
from salver.engine.scans import ScanStrategy


class SingleCollectorStrategy(ScanStrategy):
    def __init__(self, collector_name: str):
        self._collector_name = collector_name

    def run(self, facts: List[BaseFact]):
        logger.info(f"Launch single collector scan ({self._collector_name}) {facts}")
        self.run_agent_scan(queue=self._collector_name, facts=facts)
