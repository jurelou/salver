# -*- coding: utf-8 -*-
# from opulence.common.exceptions import CollectorNotFound
from opulence.engine.controllers import agents as agents_ctrl
from opulence.engine.scans.base import BaseScan

from opulence.common import models
from typing import List


class SingleCollectorConfig(models.ScanConfig):
    collector_name: str


class SingleCollector(BaseScan):
    name = "single_collector"
    config: SingleCollectorConfig

    def configure(self, config: models.ScanConfig):
        self.config = SingleCollectorConfig(**config.dict())

    def launch(self, facts: List[models.BaseFact]):
        def check_collector_exists(collector_name):
            from opulence.engine.controllers.agents import (
                available_agents,
            )  # pragma: nocover

            for agent in available_agents.values():
                if collector_name in agent:
                    return
            # raise CollectorNotFound(collector_name)
            raise ValueError(collector_name)

        check_collector_exists(self.config.collector_name)
        print("DONE")
        agents_ctrl.scan(
            "scan_id", self.config.collector_name, facts,
        )
