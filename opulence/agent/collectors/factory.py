# -*- coding: utf-8 -*-
from loguru import logger

from opulence.agent.collectors.base import BaseCollector
from opulence.agent.exceptions import (
    InvalidCollectorDefinition,
    MissingCollectorDefinition,
)
from opulence.common.factory import Factory
from opulence.config import agent_config


class CollectorFactory(Factory):
    def build(self):
        collector_modules = self.load_classes_from_module(
            root_path="opulence/agent/collectors",
            parent_class=BaseCollector,
            skip_first_level=True,
        )
        enabled_collectors = set(agent_config.collectors or [])
        collector_instances = {}
        for collector in collector_modules:
            if not hasattr(collector, "config") or not "name" in collector.config:
                raise InvalidCollectorDefinition(
                    collector_name, "Missing `name` property"
                )

            collector_name = collector.config["name"]

            # Raises if the collector name is already registered
            if collector_name in collector_instances:
                raise InvalidCollectorDefinition(collector_name, "Duplicate name found")
            if collector_name not in enabled_collectors:
                continue
            try:
                collector_instance = collector()
            except Exception as err:
                raise InvalidCollectorDefinition(collector, err)

            logger.debug(
                f"Loaded collector {collector_name} with config: {collector_instance.config}",
            )
            collector_instances[collector_name] = {
                "instance": collector_instance,
                "active": False,
            }

        for collector_name in enabled_collectors:
            if collector_name not in collector_instances:
                raise MissingCollectorDefinition(collector_name)
            collector_instances[collector_name]["active"] = True

        self.items = collector_instances
        for name, conf in collector_instances.items():
            logger.info(f"Loaded collector {name} (active: {conf['active']})")
        return collector_instances
