# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

from salver.controller import exceptions
from salver.common.models import BaseFact, ScanConfig
from salver.controller.services import agents_tasks
from salver.controller.services.agents import get_collectors_names


class BaseScan:
    name: str = ""
    config: ScanConfig = None
    scan_id: UUID = None

    @property
    def name(self):
        pass

    def configure(self, config: ScanConfig):
        self.config = config

    def scan(self, facts):
        raise NotImplementedError(f"{type(self)} does not implements `scan`")

    def launch_collector(
        self,
        collector_name: str,
        facts: List[BaseFact],
        cb=None,
    ):
        if collector_name not in get_collectors_names():
            raise exceptions.CollectorNotFound(collector_name)

        agents_tasks.scan(
            self.scan_id,
            self.config.collector_name,
            facts,
            cb=cb,
        )
