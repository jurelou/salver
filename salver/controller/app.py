#-*- coding: utf-8 -*-
from loguru import logger
from celery.signals import worker_init, worker_ready, worker_process_shutdown

from salver.config import controller_config
from salver.common.celery import create_app
from salver.controller.services import periodic_tasks
from salver.common.database.manager import DatabaseManager
from salver.controller.utils.json_encoder import json_dumps, json_loads

db_manager = DatabaseManager(
    neo4j_config=controller_config.neo4j,
    elasticsearch_config=controller_config.elasticsearch,
    mongodb_config=controller_config.mongodb,
)

# Create celery app
celery_app = create_app(json_encoder=json_loads, json_decoder=json_dumps)
celery_app.conf.update(controller_config.celery)

celery_app.conf.update(
    {
        "imports": "salver.controller.tasks",
        "task_default_queue": "controller",
    },
)


db_manager.flush()
db_manager.bootstrap()
periodic_tasks.flush()
periodic_tasks.add_periodic_task(
            celery_app,
            "salver.controller.tasks.reload_agents",
            controller_config.refresh_agents_interval,
)



# Hack for coverage.
# See: https://github.com/nedbat/coveragepy/issues/689
IS_TESTING = controller_config.ENV_FOR_DYNACONF == "testing"
if IS_TESTING:
    from coverage import Coverage # pragma: nocover
    COVERAGE = None


@worker_init.connect
def init(sender=None, conf=None, **kwargs):
    try:
        if IS_TESTING:
            global COVERAGE
            COVERAGE = Coverage(data_suffix=True)
            COVERAGE.start()

        from .tasks import reload_agents  # pragma: nocover
        reload_agents.apply()

    except Exception as err:
        logger.critical(f"Error in signal `worker_init`: {err}")



@worker_process_shutdown.connect
def on_shutdown(**kwargs):
        if IS_TESTING and COVERAGE:
            COVERAGE.stop()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            COVERAGE.save()



if __name__ == "__main__":
    argv = [
        "-A",
        "salver.controller.app",
        "worker",
        "--hostname=controller_main",
        "-B",
    ]

    celery_app.worker_main(argv)






# # -*- coding: utf-8 -*-
# from loguru import logger
# from celery.signals import worker_init, worker_ready, worker_process_init, worker_process_shutdown

# from salver.config import controller_config
# from salver.common.celery import create_app
# from salver.controller.services import periodic_tasks
# from salver.common.database.manager import DatabaseManager
# from salver.controller.utils.json_encoder import json_dumps, json_loads

# db_manager = DatabaseManager(
#     neo4j_config=controller_config.neo4j,
#     elasticsearch_config=controller_config.elasticsearch,
#     mongodb_config=controller_config.mongodb,
# )

# # Create celery app
# celery_app = create_app(json_encoder=json_loads, json_decoder=json_dumps)
# celery_app.conf.update(controller_config.celery)

# celery_app.conf.update(
#     {
#         "imports": "salver.controller.tasks",
#         "task_default_queue": "controller",
#     },
# )

# # Hack for coverage.
# # See: https://github.com/nedbat/coveragepy/issues/689
# IS_TESTING = controller_config.ENV_FOR_DYNACONF == "testing"
# if IS_TESTING:
#     from coverage import Coverage
#     COVERAGE = None

# @worker_process_init.connect
# def on_init(sender=None, conf=None, **kwargs):
#     try:
#         if IS_TESTING:
#             global COVERAGE
#             COVERAGE = Coverage(data_suffix=True)
#             COVERAGE.start()
#     except Exception as err:
#         logger.critical(f"Error in signal `worker_init`: {err}")
                

# @worker_init.connect
# def init(sender=None, conf=None, **kwargs):
#     try:
#         db_manager.flush()
#         db_manager.bootstrap()
#         periodic_tasks.flush()
#         periodic_tasks.add_periodic_task(
#             celery_app,
#             "salver.controller.tasks.reload_agents",
#             controller_config.refresh_agents_interval,
#         )
#         # debug only
#         from salver.controller import tasks  # pragma: nocover

#         tasks.reload_agents.apply()

#     except Exception as err:
#         logger.critical(f"Error in signal `worker_init`: {err}")



# @worker_process_shutdown.connect
# def on_shutdown(**kwargs):
#         if IS_TESTING and COVERAGE:
#             COVERAGE.stop()
#             print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#             COVERAGE.save()


# if __name__ == "__main__":
#     argv = [
#         "-A",
#         "salver.controller.app",
#         "worker",
#         "--hostname=controller_main",
#         "-B",
#     ]

#     celery_app.worker_main(argv)



