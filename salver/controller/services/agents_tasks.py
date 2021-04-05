# -*- coding: utf-8 -*-
from loguru import logger
from salver.controller.app import celery_app, db_manager
from typing import List
import celery
from salver.common.celery import async_call
from salver.common import models
from salver.controller.app import db_manager


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
                db_manager.update_scan_state(scan_id, models.ScanState.ERRORED)
            else:
                db_manager.update_scan_state(scan_id, models.ScanState.FINISHED)
        else:
            db_manager.update_scan_state(scan_id, models.ScanState.FINISHED)


@celery_app.task(base=CallbackTask)
def _scan_success(result, scan_id, collector_name):
    logger.info(
        f"Task success: got {len(result['facts'])} facts in {result['duration']} from {collector_name}",
    )

    scan_result = models.ScanResult(**result)
    db_manager.add_scan_results(scan_id, scan_result)
    return result, scan_id


@celery_app.task
def _scan_error(task_id, scan_id, collector_name):
    result = celery_app.AsyncResult(task_id)
    db_manager.update_scan_state(scan_id, models.ScanState.ERRORED)
    logger.critical(
        f"Unexpected error for task {task_id} from scan {scan_id} ({collector_name}) : {result.traceback} {result.state}"
    )


def scan(scan_id, collector_name: str, facts: List[models.BaseFact], cb=None):
    _scan_success.callback = cb
    logger.info(f"Collecting {collector_name} with {len(facts)} facts")

    db_manager.update_scan_state(scan_id, models.ScanState.STARTED)
    task = async_call(
        celery_app,
        "scan",
        link=_scan_success.s(scan_id, collector_name),
        link_error=_scan_error.s(scan_id, collector_name),
        queue=collector_name,
        args=[facts],
    )
    return task
