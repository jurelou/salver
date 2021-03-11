from opulence.common.exceptions import CollectorNotFound
from opulence.engine.controllers import agent_tasks
from opulence.engine.scans.base import BaseScan
from opulence.engine.scans.base import BaseScanConfig


class ScanConfig(BaseScanConfig):
    collector_name: str


class SingleCollector(BaseScan):
    name = "single_collector"
    config: ScanConfig

    def configure(self, config):
        self.config = ScanConfig(**config)

    def launch(self):
        def check_collector_exists(collector_name):
            from opulence.engine.controllers.agents import (
                available_agents,
            )  # pragma: nocover

            for agent in available_agents.values():
                if collector_name in agent:
                    return
            raise CollectorNotFound(collector_name)

        check_collector_exists(self.config.collector_name)

        agent_tasks.scan(
            self.config.external_id, self.config.collector_name, self.config.facts,
        )
