# -*- coding: utf-8 -*-
from uuid import uuid4

from loguru import logger

from opulence.common.database.neo4j import cases as neo4j_cases
from opulence.common.database.neo4j import scans as neo4j_scans
from opulence.common.models.case import Case
from opulence.common.models.scan import Scan
from opulence.engine.app import neo4j_client
from opulence.engine.controllers import agent_tasks


def create(case: Case):
    logger.info(f"Create new case: {case}")
    neo4j_cases.create(neo4j_client, case)


def add_scan(case_id: uuid4, scan_id: uuid4):
    logger.info(f"Add scan {scan_id} to case {case_id}")
    neo4j_cases.add_scan(neo4j_client, case_id=case_id, scan_id=scan_id)
