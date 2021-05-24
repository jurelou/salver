# -*- coding: utf-8 -*-
# from salver.common.exceptions import CollectorNotFound
from typing import List
from loguru import logger
from salver.common.models import ScanConfig, BaseFact
from salver.engine.scans import BaseScan


class SingleCollectorConfig(ScanConfig):
    collector_name: str


class SingleCollector(BaseScan):
    name = "single-collector"

    config: SingleCollectorConfig

    def configure(self, config: ScanConfig):
        self.config = SingleCollectorConfig(**config.dict())

    def scan(self, facts: List[BaseFact]):
        logger.info("Launch single collector scan")
        self.launch_collector(
            self.config.collector_name,
            facts
        )
