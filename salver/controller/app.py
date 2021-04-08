# -*- coding: utf-8 -*-
from celery.result import allow_join_result
from celery.signals import worker_init
from celery.signals import worker_ready
from loguru import logger

from salver.common.celery import create_app
from salver.controller.services import periodic_tasks

from salver.config import controller_config

from salver.controller.services import DatabaseManager

db_manager = DatabaseManager()
from salver.controller.utils.json_encoder import json_dumps, json_loads

# Create celery app
celery_app = create_app(json_encoder=json_loads, json_decoder=json_dumps)
celery_app.conf.update(controller_config.celery)

celery_app.conf.update(
    {
        "imports": "salver.controller.tasks", "task_eager_propagates": True,
        "task_default_queue": 'controller'
    },
)


@worker_init.connect
def init(sender=None, conf=None, **kwargs):
    try:
        db_manager.flush()
        db_manager.bootstrap()

        periodic_tasks.flush()
        periodic_tasks.add_periodic_task(
            celery_app,
            "salver.controller.tasks.reload_agents",
            controller_config.refresh_agents_interval,
        )
        # debug only
        from salver.controller import tasks  # pragma: nocover

        tasks.reload_agents.apply()

    except Exception as err:
        logger.critical(f"Error in signal `worker_init`: {err}")


@worker_ready.connect
def ready(sender=None, conf=None, **kwargs):
    print("DB_MANAGER", db_manager)
#     except Exception as err:
#         logger.critical(f"Error in signal `worker_ready`: {err}")


if __name__ == "__main__":
    argv = [
        "-A",
        "salver.controller.app",
        "worker",
        "--hostname=controller_main",
        "-B",
    ]

    celery_app.worker_main(argv)
