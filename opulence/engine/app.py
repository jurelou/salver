# -*- coding: utf-8 -*-
from celery.result import allow_join_result
from celery.signals import worker_init
from celery.signals import worker_ready
from loguru import logger

from opulence.common.celery import create_app
from opulence.engine.controllers import periodic_tasks

from opulence.config import engine_config

from opulence.engine.database.manager import DatabaseManager

db_manager = DatabaseManager()


# Create celery app
celery_app = create_app()
celery_app.conf.update(engine_config.celery)

celery_app.conf.update(
    {
        "imports": "opulence.engine.tasks",
        "task_eager_propagates": True
    }
)


@worker_init.connect
def init(sender=None, conf=None, **kwargs):
    try:
        db_manager.mongodb.flush()
        db_manager.neo4j.flush()
        # db.flush()
        db_manager.bootstrap()


        periodic_tasks.flush()
        periodic_tasks.add_periodic_task(celery_app, "opulence.engine.tasks.reload_agents", engine_config.refresh_agents_interval)

        #debug only
        from opulence.engine import tasks  # pragma: nocover
        tasks.reload_agents.apply()

    except Exception as err:
        logger.critical(f"Error in signal `worker_init`: {err}")


# @worker_ready.connect
# def ready(sender=None, conf=None, **kwargs):
#     try:
#     except Exception as err:
#         logger.critical(f"Error in signal `worker_ready`: {err}")
