from loguru import logger

from opulence.agent.collectors.base import BaseCollector
from opulence.agent.collectors.exceptions import InvalidCollectorDefinition
from opulence.common.factory import Factory
from opulence.config import agent_config


class CollectorFactory(Factory):
    def build(self):
        collector_modules = self.load_classes_from_module(
            root_path="opulence/agent/collectors",
            parent_class=BaseCollector,
            skip_first_level=True,
        )

        collector_instances = {}
        for collector in collector_modules:
            try:
                collector_instance = collector()
            except Exception as err:
                logger.critical(f"Could not load {collector}: {err}")
                continue
            collector_name = collector_instance.config.name
            if collector_name in collector_instances:
                raise InvalidCollectorDefinition(
                    f"Found collector with duplicate name `{collector_name}`.",
                )
            logger.info(
                f"Loaded collector {collector_name} with config: {collector_instance.config}"
            )
            collector_instances[collector_name] = {
                "instance": collector_instance,
                "active": False,
            }
        for collector_name in set(agent_config.collectors or []):
            if collector_name not in collector_instances:
                raise InvalidCollectorDefinition(
                    f"Can't find `{collector_name}`, which is defined in the configuration file. Check your settings.yml file `collectors` section.",
                )
            collector_instances[collector_name]["active"] = True

        self.items = collector_instances
        for name, conf in collector_instances.items():
            logger.info(f"Loaded collector {name} (active: {conf['active']})")
        return collector_instances
