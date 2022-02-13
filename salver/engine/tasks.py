from celery import current_app
from loguru import logger
import time

from salver.engine import celery_app
from salver.engine.controllers import agent_tasks
from salver.engine.agents import update_agents_list

from salver.engine.agents import get_collectors_list

@celery_app.task
def launch_scan(scan_id, facts, collector_name: str = None):
    logger.info(f"Launch scan {scan_id}, {collector_name}")

    if collector_name:
        # single collector scan
        return agent_tasks.scan(queue=collector_name, scan_id=scan_id, facts=facts)

    # full scan
    collectors = get_collectors_list()
    # some nasty race conditions may appear .., so we just retry
    if not collectors:
        time.sleep(0.5)
        collectors = get_collectors_list()
    calls = {}
    for c_name, allowed_facts in collectors.items():
        for fact in facts:
            if fact.schema()["title"] in allowed_facts:
                if c_name in calls:
                    calls[c_name].append(fact)
                else:
                    calls[c_name] = [fact]
        
    for collector, facts in calls.items():
        logger.info(f"Calling collector {collector} with {len(facts)} facts")
        agent_tasks.scan(queue=collector, scan_id=scan_id, facts=facts)


@celery_app.task(name="ping_agents")
def ping_agents():

    active_queues = current_app.control.inspect().active_queues() or {}
    agents = {}
    for name in active_queues.keys():
        conf = celery_app.control.inspect([name]).conf()[name]
        if "collectors" not in conf:
            continue
        agents[name] = conf["collectors"]
    update_agents_list(agents)
    logger.debug("updated agents")