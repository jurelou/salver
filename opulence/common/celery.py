import sys

import celery
from celery.signals import after_setup_logger, setup_logging
from kombu.serialization import register

from opulence.common import json_encoder

# class TaskRouter(object):
#     def route_for_task(self, task, *args, **kwargs):
#         if ":" not in task:
#             print("aaaaaaaaaaaaaaaaaaaaaa", task)
#             return {"queue": "default"}
#         namespace, rk = task.split(":")
#         print("===============", namespace, rk)
#         return {"queue": namespace,"routing_key": rk}


# def route_task(name, args, kwargs, options, task=None, **kw):
#         if ":" not in name:
#             print("aaaaaaaaaaaaaaaaaaaaaa", name)
#             return {"queue": "default"}
#         namespace, rk = name.split(":")
#         print("===============", namespace, rk)
#         return {"queue": namespace,"routing_key": rk}


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
