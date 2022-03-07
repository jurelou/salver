from loguru import logger

from salver.config import agent_config
from salver.common.factory import Factory
from salver.common.exceptions import InvalidCollectorDefinition
from salver.agent.collectors.base import BaseCollector


class CollectorFactory(Factory):
    def build(self):
        collector_modules = self.load_classes_from_module(
            root_path="salver/agent/collectors",
            parent_class=BaseCollector,
            skip_first_level=True,
        )

        enabled_collectors = set(agent_config.enabled_collectors or [])
        collector_instances = {}

        for collector in collector_modules:
            print("======", collector)
            collector_name = collector.config["name"]
            if collector_name not in enabled_collectors:
                continue

            try:
                collector_instance = collector()
            except Exception as err:
                raise InvalidCollectorDefinition(
                    collector_name=type(collector).__name__, error=err
                ) from err

            if collector_name in collector_instances:
                raise InvalidCollectorDefinition(
                    collector_name=collector_name,
                    error="Multiple collectors found with same name.",
                )
            collector_instances[collector_name] = {
                "instance": collector_instance,
                "enabled": collector_instance.config.name in enabled_collectors,
                "allowed_input": collector_instance.callback_types,
            }

        for enabled_collector in enabled_collectors:
            if enabled_collector not in collector_instances:
                raise InvalidCollectorDefinition(
                    collector_name=enabled_collector,
                    error="Missing required collector. Check your settings.yml",
                )

        self.items = collector_instances
        for name, conf in collector_instances.items():
            enabled = ": enabled" if conf["enabled"] else ""
            logger.info(f"Loaded collector {name}{enabled}")
        return collector_instances
