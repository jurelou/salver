# -*- coding: utf-8 -*-
import pytest
import subprocess
import time
import os
import signal
from salver.controller import tasks


@pytest.fixture(scope="session", autouse=True)
def salver_simple_deployment(request):
    proc_agent = subprocess.Popen(
        ["python", "-m", "salver.agent.app"], preexec_fn=os.setsid
    )
    proc_engine = subprocess.Popen(
        ["python", "-m", "salver.controller.app"], preexec_fn=os.setsid
    )

    def wait_for_engine():
        while True:
            time.sleep(1)
            if tasks.ping.delay().get():
                return tasks.reload_agents.delay().get()

    request.addfinalizer(lambda: os.killpg(os.getpgid(proc_agent.pid), signal.SIGKILL))
    request.addfinalizer(lambda: os.killpg(os.getpgid(proc_engine.pid), signal.SIGKILL))
    wait_for_engine()
