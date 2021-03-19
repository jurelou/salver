# -*- coding: utf-8 -*-
from opulence.engine.app import celery_app as engine_app
import pytest
from opulence.engine.database.manager import DatabaseManager


@pytest.fixture(scope="module")
def celery_app(request):
    # engine_app.conf.update(task_always_eager=True)
    return engine_app


@pytest.fixture(scope="class")
def database_manager(request):
    manager = DatabaseManager()
    manager.flush()
    manager.bootstrap()
    request.cls.database_manager = manager
