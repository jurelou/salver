from celery import Celery
from kombu.serialization import register

from . import jsonEncoder


def configure_celery(config, custom_encoder=True, **kwargs):
    app = Celery(__name__, **kwargs)
    config.update(
        {
            "task_routes": ("opulence.common.celery.taskRouter.TaskRouter",),
            "accept_content": ["customEncoder", "application/json"],
            "task_serializer": "customEncoder",
            "result_serializer": "customEncoder",
        }
    )
    app.conf.update(config)
    if custom_encoder:
        register(
            "customEncoder",
            jsonEncoder.custom_dumps,
            jsonEncoder.custom_loads,
            content_type="application/x-customEncoder",
            content_encoding="utf-8",
        )
    return app
