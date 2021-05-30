# -*- coding: utf-8 -*-
# from salver.common.exceptions import CollectorNotFound
from typing import List

from loguru import logger

from salver.engine.scans import BaseScan
from salver.common.models import BaseFact, ScanConfig
from salver.engine.services.agents import get_collectors_mapping


class FullScanConfig(ScanConfig):
    pass


class FullScan(BaseScan):
    name = 'full-scan'

    config: FullScanConfig

    def configure(self, config: ScanConfig):
        self.config = FullScanConfig(**config.dict())

    @staticmethod
    def _get_available_collectors(facts: List[BaseFact]):
        available_collectors = get_collectors_mapping()

        mapping = {}
        for fact in facts:
            fact_type = fact.schema()['title']
            if fact_type not in available_collectors:
                continue
            for collector in available_collectors[fact_type]:
                if collector in mapping:
                    mapping[collector].append(fact)
                else:
                    mapping[collector] = [fact]

        return mapping

    def scan(self, facts: List[BaseFact]):
        logger.debug('Launch full scan')

        collects = self._get_available_collectors(facts)
        for collector, facts in collects.items():
            self.launch_collector(collector, facts)
