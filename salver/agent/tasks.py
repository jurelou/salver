# -*- coding: utf-8 -*-
from timeit import default_timer as timer

from loguru import logger

from salver.common import models
from salver.common.kafka import ConsumerCallback
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
        self.collect_response_producer = kafka_producers.make_collect_response()

    def on_message(self, collect):
        logger.info(f'Got agent collect: {collect}')
        if collect.collector_name not in self.enabled_collectors:
            logger.warning(
                f'Collector {collect.collector_name} does not exists (or not enabled).',
            )
            return

        start_time = timer()
        collect_output = self.enabled_collectors[collect.collector_name].collect(
            collect.facts,
        )
        elapsed_time = timer() - start_time
        for out in collect_output:
            if isinstance(out, models.BaseFact):
                a = models.CollectResponse(
                    collect_id=collect.external_id,
                    scan_id=collect.scan_id,
                    fact=out
                )
                print("@@@@@@@@@@@", a)
                self.collect_response_producer.produce(a)