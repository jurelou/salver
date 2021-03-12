from typing import List

from celery import current_task
from loguru import logger

from opulence.agent.app import celery_app
from opulence.agent.app import es_client
from opulence.agent.collectors.factory import CollectorFactory
from opulence.agent import exceptions
from opulence.common.database.es import facts as facts_index
from opulence.common.models.fact import BaseFact

all_collectors = CollectorFactory().items

# @celery_app.task
# def toto():
#     logger.info("OOOOOOOOOOOO")
#     print("GOOGOGOOGOG")


@celery_app.task(name="scan", throws=(exceptions.BaseAgentException))
def scan(facts: List[BaseFact]):
    try:
        collector_name = current_task.request.delivery_info["routing_key"]

        if collector_name not in all_collectors:
            raise exceptions.sllectorNotFound(f"Collector {collector_name} not found.")
        if not all_collectors[collector_name]["active"]:
            raise exceptions.CollectorDisabled(
                f"Collector {collector_name} is not enabled.",
            )

        collect_result = all_collectors[collector_name]["instance"].collect(facts)

        facts_index.bulk_upsert(es_client, collect_result.facts)
        result = collect_result.dict(exclude={"facts"})
        result["facts"] = [fact.hash__ for fact in collect_result.facts]

    except Exception as err:
        logger.critical(err)
    return result
