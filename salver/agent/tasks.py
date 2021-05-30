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
        logger.info(f'Got engine connect: {engine_info.name}')
        self.agent_connect.produce(self.agent_info, flush=True)


class OnCollect(ConsumerCallback):
    def __init__(self, enabled_collectors):
        self.enabled_collectors = enabled_collectors
        self.collect_response_p = kafka_producers.make_collect_response()
        self.collect_finished_p = kafka_producers.make_collect_done()
        self.error_p = kafka_producers.make_error()

    def execute_collector(self, collect: models.Collect):
        start_time = timer()
        collect_output = self.enabled_collectors[collect.collector_name].collect(
            collect.external_id.hex,
            collect.facts,
        )
        state = models.CollectState.FINISHED
        facts_count = 0
        for out in collect_output:
            if isinstance(out, models.BaseFact):
                self.collect_response_p.produce(
                    models.CollectResult(
                        collect_id=collect.external_id,
                        scan_id=collect.scan_id,
                        fact=out,
                        collector_name=collect.collector_name,
                    ),
                )
                facts_count = facts_count + 1
            else:
                state = models.CollectState.ERRORED
                self.error_p.produce(out)
                logger.error(f'OnCollect error: {out.error}')

        elapsed_time = timer() - start_time
        return state, elapsed_time, facts_count

    def on_message(self, collect):
        logger.info(f'Got collect for {collect.collector_name}')
        if collect.collector_name not in self.enabled_collectors:
            error = (
                f'Collector {collect.collector_name} does not exists (or not enabled).'
            )
            logger.warning(error)
            return self.error_p.produce(
                models.Error(
                    context=f'agent-collect.collector_not_found',
                    error=error,
                    collect_id=collect.external_id.hex,
                    collector_name=collect.collector_name,
                ),
            )

        state, elapsed_time, facts_count = self.execute_collector(collect)
        self.collect_finished_p.produce(
            models.CollectDone(
                collect_id=collect.external_id,
                state=state,
                facts_count=facts_count,
                duration=elapsed_time,
                collector_name=collect.collector_name,
            ),
        )
