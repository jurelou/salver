# -*- coding: utf-8 -*-
from typing import List
from uuid import uuid4

from loguru import logger

from opulence.common.database.neo4j import scans as neo4j_scans
from opulence.common.models.scan import Scan
from opulence.engine.app import neo4j_client
from opulence.engine.controllers import fact as fact_ctrl
from opulence.engine.scans.factory import ScanFactory

all_scans = ScanFactory().build()
# from opulence.engine.app import celery_app


def schedule():
    # from opulence.engine.controllers.periodic_tasks import add_periodic_task
    add_periodic_task(
        app=celery_app, interval=1, task_path="opulence.engine.tasks.toto",
    )


# def create(scan: Scan):
#     logger.info(f"Create scan {scan}")
#     neo4j_scans.create(neo4j_client, scan)


# def add_facts(scan_id: uuid4, facts_ids: List[uuid4]):
#     logger.info(f"Add collected facts {facts_ids} to scan {scan_id}")

#     neo4j_scans.add_facts(neo4j_client, scan_id, facts_ids, relationship="collects")


# def add_user_input_facts(scan_id: uuid4, facts_ids: List[uuid4]):
#     logger.info(f"Add user input facts {facts_ids} to scan {scan_id}")
#     neo4j_scans.add_facts(neo4j_client, scan_id, facts_ids, relationship="consists_of")


# def get(scan_id: uuid4):
#     logger.info(f"Get scan {scan_id}")
#     scan = neo4j_scans.get(neo4j_client, scan_id)

#     facts = neo4j_scans.get_user_input_facts(neo4j_client, scan_id)
#     scan.facts = fact_ctrl.get_many(facts)
#     return scan


def launch(scan: Scan):
    logger.info(f"Launch scan {scan.external_id} of type {scan.scan_type}")

    if scan.scan_type not in all_scans:
        logger.error(f"Scan {scan.scan_type} not found")
        raise ValueError(f"Scan {scan.scan_type} not found")

    scan_class = all_scans[scan.scan_type]()

    scan_config = scan.dict(exclude={"timestamp", "scan_type", "facts"})
    scan_config["facts"] = scan.facts
    scan_class.configure(scan_config)
    scan_class.launch()
