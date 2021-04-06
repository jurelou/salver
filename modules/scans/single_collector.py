# -*- coding: utf-8 -*-
# from salver.common.exceptions import CollectorNotFound
from salver.controller.services import agents as agents_ctrl
from salver.controller.scans.base import BaseScan
from salver.controller.app import celery_app
from salver.common import models
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
        a = self.launch_collector(
            self.config.collector_name, facts, cb=self.scan_success_lol,
        )

        print("!!!!", a)
