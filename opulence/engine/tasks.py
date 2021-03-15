from uuid import uuid4

from celery.schedules import schedule
from loguru import logger

from opulence.common.models.case import Case
from opulence.common.models.scan import Scan
from opulence.config import engine_config
from opulence.engine.app import celery_app
# from opulence.engine.controllers import agents as agents_ctrl
# from opulence.engine.controllers import case as case_ctrl
# from opulence.engine.controllers import fact as fact_ctrl
# from opulence.engine.controllers import periodic_tasks
# from opulence.engine.controllers import scan as scan_ctrl


@celery_app.task
def toto():
    print("TOTO Task")


@celery_app.task
def reload_periodic_tasks():
    periodic_tasks.flush()
    periodic_tasks.add_periodic_task(
        app=celery_app,
        interval=schedule(run_every=engine_config.refresh_agents_interval),
        task_path="opulence.engine.tasks.reload_agents",
    )


@celery_app.task
def reload_agents():
    logger.debug("Reloading agents")
    agents_ctrl.refresh_agents()


@celery_app.task
def add_case(case: Case):
    logger.debug(f"Add new case: {case}")
    case_ctrl.create(case)


@celery_app.task
def add_scan(case_id: uuid4, scan: Scan):
    logger.debug(f"Add scan {scan} to case {case_id}")

    scan_ctrl.create(scan)
    case_ctrl.add_scan(case_id, scan.external_id)

    fact_ctrl.add_many(scan.facts)
    facts_ids = [fact.hash__ for fact in scan.facts]

    scan_ctrl.add_user_input_facts(scan.external_id, facts_ids)


@celery_app.task
def launch_scan(scan_id: uuid4):
    logger.debug(f"Launch scan {scan_id}")

    try:
        scan = scan_ctrl.get(scan_id)
        scan_ctrl.launch(scan)

    except Exception as err:
        import sys
        import traceback

        traceback.print_exc(file=sys.stdout)
        logger.critical(err)
    # scan_ctrl.create(scan)
    # case_ctrl.add_scan(case_id, scan.external_id)


@celery_app.task
def schedule_scan(scan_id: uuid4):
    logger.debug(f"Schedule scan {scan_id}")
    scan = scan_ctrl.get(scan_id)
    scan_ctrl.schedule(scan)


# a = tasks.test_agent.apply_async().get()
# print("@@@@@@@@@@@@@@@@@@@")
# print("res->", a)
# print("@@@@@@@@@@@@@@@@@")


# @celery_app.task(name="engine.scan.launch")
# def scan(scan_type: str, config: BaseFact):
#   print("!!!!!!ENGINE TOTO")


# from opulence.engine import remote_tasks
# from opulence.facts.person import Person
# from opulence.common.celery import sync_call
# from opulence.agent import celery_app


# a = tutu.signature("agent_scan:agent.scan.launch", ["azeazeaze", Person(firstname="lol", lastname="mdr")])

# a.apply_async()

# a = tutu.send_task("agent_scan:agent.scan.launch", ["azeazeaze", Person(firstname="lol", lastname="mdr")])
#
# a.get()

# a = remote_tasks.launch_scan("b-collector", [Person(firstname="lol", lastname="mdr")]).apply_async()
# print("@@@@", a.get())
