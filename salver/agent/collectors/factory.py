# -*- coding: utf-8 -*-
from loguru import logger

from salver.config import agent_config
from salver.common.factory import Factory
from salver.agent.exceptions import (
    InvalidCollectorDefinition,
    MissingCollectorDefinition,
)
from salver.agent.collectors.base import BaseCollector

ENABLED_COLLECTORS = set(agent_config.enabled_collectors) or []


class CollectorFactory(Factory):
    def _check_collector(self, collector):
        # Collectors should have a config dict
        if not hasattr(collector, "config"):
            raise InvalidCollectorDefinition(
                collector,
                "Missing config",
            )

        if "name" not in collector.config:
            raise InvalidCollectorDefinition(
                collector,
                "Missing `name` property",
            )

        collector_name = collector.config["name"]

        # Checks for duplicate collector names
        if collector_name in self.items:
            raise InvalidCollectorDefinition(
                collector_name,
                f"Duplicate name {collector_name} found",
            )

        if collector_name not in ENABLED_COLLECTORS:
            return collector_name, {
                "instance": None,
                "active": False,
            }
        try:
            collector_instance = collector()
        except Exception as err:
            raise InvalidCollectorDefinition(collector, err)

        # logger.debug(
        #     f'Loaded collector {collector_name} \
        #     active: {} with config: {collector_instance.config}',
        # )
        return collector_name, {
            "instance": collector_instance,
            "active": True,
        }

    def build(self):
        collector_modules = self.load_classes_from_module(
            root_path=agent_config.collectors_path,
            parent_class=BaseCollector,
        )
        print("!!!!", collector_modules)

        self.items = {}
        for collector in collector_modules:
            collector_name, collector_config = self._check_collector(collector)
            self.items[collector_name] = collector_config
            logger.info(
                f"Loaded collector {collector_name} active: {collector_config['active']}",
            )

        for collector_name in ENABLED_COLLECTORS:
            if collector_name not in self.items:
                logger.critical(
                    f"Collector {collector_name} not found, but it was defined in the settings.yml",
                )
                raise MissingCollectorDefinition(collector_name)

        return self.items
