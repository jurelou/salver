# -*- coding: utf-8 -*-
from uuid import UUID

from loguru import logger

from salver.controller import models, exceptions
from salver.common.models import ScanState
from salver.controller.app import celery_app, db_manager
from salver.controller.services import scans, agents, agents_tasks

# from celery.schedules import schedule


@celery_app.task
def ping():
    logger.info("Ping")
    return "pong"


# @celery_app.task
# def ping_agents():


@celery_app.task
def list_agents():
    logger.info("List agents")
    return [
        models.Agent(name=name, collectors=collectors)
        for name, collectors in agents.AVAILABLE_AGENTS.items()
    ]


@celery_app.task
def reload_agents():
    logger.info("Reload agents")
    agents.refresh_agents()


@celery_app.task
def launch_scan(scan_id: UUID):
    logger.info(f"Launch scan {scan_id}")

    scan = db_manager.get_scan(scan_id)
    db_manager.update_scan_state(scan.external_id, ScanState.STARTING)
    scan_facts = db_manager.get_input_facts_for_scan(scan_id)
    scans.launch(scan, scan_facts)
