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
from salver.engine.services.agents import get_collectors_mapping


class FullScanConfig(ScanConfig):
    pass

<<<<<<< HEAD

class FullScan(BaseScan):
    name = 'full-scan'
=======
class FullScan(BaseScan):
    name = "full-scan"
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

    config: FullScanConfig

    def configure(self, config: ScanConfig):
        self.config = FullScanConfig(**config.dict())

    @staticmethod
    def _get_available_collectors(facts: List[BaseFact]):
        available_collectors = get_collectors_mapping()
<<<<<<< HEAD

        mapping = {}
        for fact in facts:
            fact_type = fact.schema()['title']
=======
        
        mapping = {}
        for fact in facts:
            fact_type = fact.schema()["title"]            
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
            if fact_type not in available_collectors:
                continue
            for collector in available_collectors[fact_type]:
                if collector in mapping:
                    mapping[collector].append(fact)
                else:
                    mapping[collector] = [fact]

        return mapping

    def scan(self, facts: List[BaseFact]):
<<<<<<< HEAD
        logger.debug('Launch full scan')
=======
        logger.info("Launch full scan")
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96

        collects = self._get_available_collectors(facts)
        for collector, facts in collects.items():
            self.launch_collector(collector, facts)
