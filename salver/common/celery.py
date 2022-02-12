from celery import Celery
from kombu.serialization import register

from salver.common.json_encoder import custom_dumps, custom_loads

class TaskRouter(object):
    def route_for_task(self, task, *args, **kwargs):
        if ":" not in task:
            return {"queue": "default"}
        namespace, _ = task.split(":")
        return {"queue": namespace}

def configure_celery(config, **kwargs):
    register(
        "customEncoder",
        custom_dumps,
        custom_loads,
        content_type="application/x-customEncoder",
        content_encoding="utf-8",
    )
    app = Celery(__name__, **kwargs)
    config.update(
        {
            #"task_routes": (TaskRouter,),
            "accept_content": ["customEncoder", "application/json"],
            "task_serializer": "customEncoder",
            "result_serializer": "customEncoder",
        }
    )
    app.conf.update(config)
    return app