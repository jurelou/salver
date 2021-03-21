# -*- coding: utf-8 -*-
import sys

import celery
from celery.signals import after_setup_logger
from celery.signals import setup_logging
from kombu.serialization import register

from opulence.common import json_encoder


def create_app():
    register(
        "customEncoder",
        json_encoder.json_dumps,
        json_encoder.json_loads,
        content_type="application/x-customEncoder",
        content_encoding="utf-8",
    )
    celery_app = celery.Celery(__name__)
    celery_app.conf.update(
        {
            #   "task_routes": (route_task,),
            "accept_content": ["customEncoder", "application/json"],
            "task_serializer": "customEncoder",
            "result_serializer": "customEncoder",
            "worker_hijack_root_logger": False,
        },
    )
    return celery_app


@setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


# @after_setup_logger.connect
# def setup_loggers(logger, *args, **kwargs):
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#     # FileHandler
#     fh = logging.FileHandler('logs.log')
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)


def async_call(app, task_path, **kwargs):
    return app.send_task(task_path, **kwargs)
