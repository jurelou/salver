# -*- coding: utf-8 -*-
from celery.result import allow_join_result
from celery.signals import worker_init
from celery.signals import worker_ready
from loguru import logger

from opulence.common.celery import create_app
from opulence.engine.controllers import periodic_tasks

# from opulence.common.database.es import utils as es_utils
# from opulence.common.database.neo4j import utils as neo4j_utils
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


@worker_ready.connect
def ready(sender=None, conf=None, **kwargs):
    try:

        from opulence.engine import tasks  # pragma: nocover

        from opulence.common.models.case import Case
        from opulence.common.models.scan import Scan

        from opulence.facts.company import Company
        from opulence.facts.domain import Domain
        from opulence.facts.person import Person
        from opulence.facts.phone import Phone
        from opulence.facts.username import Username
        from opulence.facts.email import Email

        case = Case(name="tata")

        scan = Scan(
            case_id=case.external_id,
            facts=[
                Phone(number="+33123123"),
                Phone(number="+33689181869"),
                Username(name="jurelou"),
                Company(name="wavely"),
                Domain(fqdn="wavely.fr"),
                Person(
                    firstname="fname",
                    lastname="lname",
                    anther="ldm",
                    first_seen=42,
                    last_seen=200,
                ),
                Email(address="test@gmail.test"),
            ],
            scan_type="single_collector",
            config={"collector_name": "dummy-docker-collector"},
        )


        a = db_manager.add_case(case)
        a = db_manager.add_scan(scan)

        case = db_manager.get_scan(scan.external_id)

        tasks.launch_scan.apply(args=[scan.external_id])

    except Exception as err:
        logger.critical(f"Error in signal `worker_ready`: {err}")
