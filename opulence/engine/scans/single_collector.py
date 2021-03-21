# -*- coding: utf-8 -*-
# from opulence.common.exceptions import CollectorNotFound
from opulence.engine.controllers import agents as agents_ctrl
from opulence.engine.scans.base import BaseScan
from opulence.engine.app import celery_app
from opulence.common import models
from typing import List


class SingleCollectorConfig(models.ScanConfig):
    collector_name: str

class SingleCollector(BaseScan):
    name = "single_collector"
    config: SingleCollectorConfig

    def configure(self, config: models.ScanConfig):
        self.config = SingleCollectorConfig(**config.dict())

    def scan_success_lol(self, result):
        print("CALLBACKKKKKKKKKKKKK", result) 

    def scan(self, facts: List[models.BaseFact]):
        self.launch_collector(self.config.collector_name, facts, cb=self.scan_success_lol)
