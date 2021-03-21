# -*- coding: utf-8 -*-
import pytest
from opulence.engine.database.manager import DatabaseManager


@pytest.fixture(scope="class")
def engine_app(request):
    from opulence.engine.app import celery_app

    celery_app.conf.update(task_eager_propagates=True)
    # celery_app.conf.update(task_always_eager=True)
    return celery_app


@pytest.fixture(scope="class")
def agent_app(request):
    from opulence.agent.app import celery_app

    # celery_app.conf.update(task_always_eager=True)
    celery_app.conf.update(task_eager_propagates=True)
    return celery_app


@pytest.fixture(scope="class")
def database_manager(request):
    manager = DatabaseManager()
    manager.flush()
    manager.bootstrap()
    request.cls.database_manager = manager
