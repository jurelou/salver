# -*- coding: utf-8 -*-
from typing import List

import celery
from loguru import logger

from salver.common.celery import async_call
from salver.common.models import BaseFact, ScanState, ScanResult
from salver.controller.app import celery_app, db_manager


def ping():
    from salver.facts import Person

    task = async_call(
        celery_app,
        "ping",
        args=[Person(firstname="f", lastname="l")],
        queue="zen",
    )
    print("-----", task)
    return task


class CallbackTask(celery.Task):
    callback = None

    def on_failure(self, exc, task_id, args, kwargs, einfo):  # pragma: no cover
        logger.critical(f"ERROR {exc} {task_id} {args} {kwargs} {einfo}")

    def on_success(self, retval, task_id, *args, **kwargs):
        result, scan_id = retval
        if self.callback:
            try:
                logger.info(f"Calling callback {self.callback.__func__}")
                self.callback(result)
            except Exception as err:
                logger.critical(f"Callback error: {err}")
                db_manager.update_scan_state(scan_id, ScanState.ERRORED)
                return
        db_manager.update_scan_state(scan_id, ScanState.FINISHED)


@celery_app.task(base=CallbackTask)
def _scan_success(result, scan_id, collector_name):
    logger.info(
        f"Task success: got {len(result['facts'])} facts in \
        {result['duration']} from {collector_name}",
    )
    try:
        scan_result = ScanResult(**result)
        db_manager.add_scan_results(scan_id, scan_result)
    except Exception as err:
        print("ERR SCAN SUCCESS", err)
    return result, scan_id


@celery_app.task
def _scan_error(task_id, scan_id, collector_name):
    result = celery_app.AsyncResult(task_id)
    print("#############ERRRRRRRRRRRRRRRRR")
    db_manager.update_scan_state(scan_id, ScanState.ERRORED)
    logger.critical(
        f"Unexpected error for task {task_id} from scan {scan_id}  \
        ({collector_name}) : {result.traceback} {result.state}",
    )


def scan(scan_id, collector_name: str, facts: List[BaseFact], cb=None):
    _scan_success.callback = cb
    logger.info(f"Collecting {collector_name} with {len(facts)} facts")
    db_manager.update_scan_state(scan_id, ScanState.STARTED)

    task = async_call(
        celery_app,
        "scan",
        link=_scan_success.s(scan_id, collector_name).set(queue="controller"),
        link_error=_scan_error.s(scan_id, collector_name).set(queue="controller"),
        queue=collector_name,
        args=[facts],
    )

    print("!!!!!", task)
    return task
