# -*- coding: utf-8 -*-
from typing import List

from celery import current_task
from loguru import logger

from opulence.agent.app import celery_app
from opulence.agent.app import es_client
from opulence.agent.collectors.factory import CollectorFactory
from opulence.agent import exceptions
from opulence.common.models.fact import BaseFact

all_collectors = CollectorFactory().items

# @celery_app.task
# def toto():
#     logger.info("OOOOOOOOOOOO")
#     print("GOOGOGOOGOG")


from elasticsearch.helpers import bulk
from opulence.facts import all_facts


__facts_index_mapping = [(fact, f"facts_{fact.lower()}") for fact in all_facts.keys()]
fact_to_index = lambda fact: [i for f, i in __facts_index_mapping if f == fact][0]


def bulk_upsert(client, facts):
    def gen_actions(facts):
        logger.info(f"Upsert fact: {len(facts)}")
        for fact in facts:
            yield {
                "_op_type": "update",
                "_index": fact_to_index(fact.schema()["title"]),
                "_id": fact.hash__,
                "upsert": fact.dict(exclude={"hash__"}),
                "doc": fact.dict(exclude={"first_seen", "hash__"}),
            }

    bulk(client=client, actions=gen_actions(facts))


@celery_app.task(name="scan", throws=(exceptions.AgentException))
def scan(facts: List[BaseFact]):
    try:
        collector_name = current_task.request.delivery_info["routing_key"]

        if collector_name not in all_collectors:
            raise exceptions.CollectorNotFound(collector_name)
        if not all_collectors[collector_name]["active"]:
            raise exceptions.CollectorDisabled(collector_name,)

        collect_result = all_collectors[collector_name]["instance"].collect(facts)

        bulk_upsert(es_client, collect_result.facts)
        result = collect_result.dict(exclude={"facts"})
        result["facts"] = [fact.hash__ for fact in collect_result.facts]

    except Exception as err:
        logger.critical(err)
    return result
