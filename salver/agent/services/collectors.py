# -*- coding: utf-8 -*-
from loguru import logger

from salver.config import agent_config
from salver.common.utils import load_classes
from salver.agent.exceptions import MissingCollectorDefinition
from salver.common.collectors import BaseCollector

from salver.common.collectors.exceptions import (
    InvalidCollectorDefinition,
    MissingCollectorDefinition,
)


def build():
    enabled_collectors = set(agent_config.enabled_collectors or [])
    collector_modules = load_classes(
        root_path='salver/agent/collectors',
        parent_class=BaseCollector,
    )
    collectors = {}
    for collector in collector_modules:
        try:
            instance = collector()
            collectors[instance.config.name] = {
                'instance': instance,
                'enabled': instance.config.name in enabled_collectors,
            }
        except InvalidCollectorDefinition as err:
            print(f'Could not load {collector}: {err}')

    for enabled_collector in enabled_collectors:
        if enabled_collector not in collectors:
            raise MissingCollectorDefinition(enabled_collector)
    return collectors


ALL_COLLECTORS = build()
