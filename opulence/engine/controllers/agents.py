# -*- coding: utf-8 -*-
from loguru import logger

from opulence.config import engine_config
from opulence.engine.app import celery_app

from typing import List

# from celery.result import allow_join_result

from opulence.common.celery import async_call
from opulence.common.models import BaseFact
import multiprocessing
# from opulence.engine.controllers.scan import add_facts
# from opulence.engine.controllers.fact import add_many, get_many

manager = multiprocessing.Manager()
available_agents = manager.dict()

get_agents = lambda : available_agents

def refresh_agents():
    global available_agents

    def _get_agents():
        workers = celery_app.control.inspect().active_queues() or {}
        for name in workers.keys():
            conf = celery_app.control.inspect([name]).conf()[name]
            if "collectors" in conf:
                yield name, conf["collectors"]

    available_agents = {agent: config for agent, config in _get_agents()}
    logger.info(f"Available agents: {available_agents.keys()}")


@celery_app.task(ignore_result=True, acks_late=True)
def scan_success(result, scan_id):
    try:
        logger.info(
            f"Task success: got {len(result['facts'])} facts in {result['duration']}",
        )
        # print(result)
        # add_many(get_many(result["facts"]))
        # add_facts(scan_id, result["facts"])
    except Exception as err:
        logger.critical(err)


@celery_app.task
def scan_error(task_id, collector_name):
    logger.error(f"Task {task_id} error")
    # with allow_join_result():
    #     print("ERROR", task_id, collector_name)
    # result = celery_app.AsyncResult(task_id)
    # print("result ->", result.state)
    # print("result ->", result.get())

    # try:
    #     log.info("file:%s probe %s", file, probe)
    #     with session_query() as session:
    #         result = probe_ctrl.create_error_results(probe, "job error",
    #                                                  session)
    #         celery_frontend.scan_result(file, probe, result)
    # except Exception as e:
    #     log.exception(type(e).__name__ + " : " + str(e))
    #     raise job_error.retry(countdown=5, max_retries=3, exc=e)


def scan(scan_id, collector_name: str, facts: List[BaseFact]):
    logger.info(f"Collecting {collector_name} with {len(facts)} facts")
    task = async_call(
        celery_app,
        "scan",
        link=scan_success.signature([scan_id]),
        link_error=scan_error.signature([collector_name]),
        queue=collector_name,
        args=[facts],
    )
    return task
