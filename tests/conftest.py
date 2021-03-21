# -*- coding: utf-8 -*-
import pytest
import subprocess
import os

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

@pytest.fixture(scope="class", autouse=True)
def agent_worker(request):
    proc_agent = subprocess.Popen(["python", "-m", "opulence.agent.app"])

    import time
    time.sleep(2)
    proc_engine = subprocess.Popen(["python", "-m", "opulence.engine.app"])
    def kill_agent():
        proc_agent.terminate()
    def kill_engine():
        proc_engine.terminate()

    request.addfinalizer(kill_agent)
    request.addfinalizer(kill_engine)

    time.sleep(2)

    # request.addfinalizer(proc_engine.kill)
    time.sleep(2)



@pytest.fixture(scope="class")
def database_manager(request):
    from opulence.engine.database.manager import DatabaseManager

    manager = DatabaseManager()
    manager.flush()
    manager.bootstrap()
    request.cls.database_manager = manager

