# -*- coding: utf-8 -*-
from timeit import default_timer as timer

from loguru import logger

from salver.common.kafka import ConsumerCallback

# from salver.agent.api import AgentAPI
from salver.agent.services import kafka_producers


class OnEngineConnect(ConsumerCallback):
    def __init__(self, agent_info):
        self.agent_connect = kafka_producers.make_agent_connect()
        self.agent_info = agent_info

    def on_message(self, engine_info):
        logger.info(f'Got engine connect: {engine_info}')
        self.agent_connect.produce(self.agent_info, flush=True)


class OnCollect(ConsumerCallback):
    def __init__(self, enabled_collectors):
        self.enabled_collectors = enabled_collectors

    def on_message(self, collect):
        logger.info(f'Got agent collect: {collect}')
        if collect.collector_name not in self.enabled_collectors:
            logger.warning(
                f'Collector {collect.collector_name} does not exists (or not enabled).',
            )
            return

        start_time = timer()
        output_facts = self.enabled_collectors[collect.collector_name].collect(
            collect.facts,
        )
        elapsed_time = timer() - start_time
        print('!!!!!!!!!!!!!!!', output_facts)
