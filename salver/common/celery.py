# -*- coding: utf-8 -*-

import celery
from celery.signals import setup_logging
from kombu.serialization import register

from salver.common import json_encoder as default_encoder


def create_app(json_encoder=None, json_decoder=None):
    if not json_decoder:
        json_decoder = default_encoder.json_dumps
    if not json_encoder:
        json_encoder = default_encoder.json_loads
    register(
        "customEncoder",
        json_decoder,
        json_encoder,
        content_type="application/x-customEncoder",
        content_encoding="utf-8",
    )
    celery_app = celery.Celery(__name__)
    celery_app.conf.update(
        {
            "accept_content": ["customEncoder", "application/json"],
            "task_serializer": "customEncoder",
            "result_serializer": "customEncoder",
            "worker_hijack_root_logger": False,
        },
    )
    return celery_app


@setup_logging.connect
def on_celery_setup_logging(**kwargs):  # pragma: no cover
    pass


def async_call(app, task_path, **kwargs):
    return app.send_task(task_path, **kwargs)


def sync_call(app, task_path, **kwargs):
    t = app.send_task(task_path, **kwargs)
    return t.get()
