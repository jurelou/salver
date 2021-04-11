from salver.config import api_config
from salver.common.celery import create_app
from salver.controller.utils.json_encoder import json_dumps, json_loads

# Create celery app
controller_app = create_app(json_encoder=json_loads, json_decoder=json_dumps)
controller_app.conf.update(api_config.celery)


def async_call(task_name, **kwargs):
    return controller_app.send_task(task_name, **kwargs)


def sync_call(task_name, timeout=10, **kwargs):
    task = async_call(task_name, **kwargs)
    return task.get(timeout=timeout)
