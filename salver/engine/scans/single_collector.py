# -*- coding: utf-8 -*-
# from salver.common.exceptions import CollectorNotFound
from typing import List

from salver.common.models import ScanConfig, BaseFact
from salver.engine.scans import BaseScan


class SingleCollectorConfig(ScanConfig):
    collector_name: str


class SingleCollector(BaseScan):
    name = "single_collector"

    config: SingleCollectorConfig

    def configure(self, config: ScanConfig):
        self.config = SingleCollectorConfig(**config.dict())

    def scan(self, facts: List[BaseFact]):
        print("SCANNNNNNN", facts)
        self.launch_collector(
            self.config.collector_name,
            facts
        )
