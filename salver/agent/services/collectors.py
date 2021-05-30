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
<<<<<<< HEAD
                'allowed_input': instance.callback_types,
=======
                'allowed_input': instance.callback_types
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
            }
        except InvalidCollectorDefinition as err:
            logger.error(f'Could not load {collector}: {err}')

    for enabled_collector in enabled_collectors:
        if enabled_collector not in collectors:
            raise MissingCollectorDefinition(enabled_collector)

    for collector_name, collector_config in collectors.items():
        enabled = ': enabled' if collector_config['enabled'] else ''
        logger.info(f'Loaded collector {collector_name} -> {enabled}')
    return collectors
