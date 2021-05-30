# -*- coding: utf-8 -*-
# from salver.common.exceptions import CollectorNotFound
from typing import List
<<<<<<< HEAD

from loguru import logger

from salver.engine.scans import BaseScan
from salver.common.models import BaseFact, ScanConfig
=======
from loguru import logger
from salver.common.models import ScanConfig, BaseFact
from salver.engine.scans import BaseScan
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96


class SingleCollectorConfig(ScanConfig):
    collector_name: str


class SingleCollector(BaseScan):
<<<<<<< HEAD
    name = 'single-collector'
=======
    name = "single-collector"
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

    config: SingleCollectorConfig

    def configure(self, config: ScanConfig):
        self.config = SingleCollectorConfig(**config.dict())

    def scan(self, facts: List[BaseFact]):
<<<<<<< HEAD
        logger.debug('Launch single collector scan')
        self.launch_collector(self.config.collector_name, facts)
=======
        logger.info("Launch single collector scan")
        self.launch_collector(
            self.config.collector_name,
            facts
        )
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
