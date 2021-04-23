
# -*- coding: utf-8 -*-
import pytest
import subprocess
import time
import os
import signal
from salver.controller import tasks
from .datasets import boot

from multiprocessing import Process

from salver.agent.app import celery_app as agent_app
from salver.controller.app import celery_app as controller_app

def start_agent():
    argv = [
        "-A",
        "salver.agent.app",
        "worker",
        "--hostname=agent_main",
        # "--concurrency=4"

    ]
    agent_app.worker_main(argv)

def start_controller():
    argv = [
        "-A",
        "salver.controller.app",
        "worker",
        "--hostname=controller_main",
        "-B",
        # "--concurrency=4"
    ]

    controller_app.worker_main(argv)

@pytest.fixture(scope='session', autouse=True)
def salver_simple_deployment(request):

    # env = os.environ.copy()

    # proc_agent = subprocess.Popen(
    #     ['python', '-m', 'salver.agent.app'], preexec_fn=os.setsid, env=env
    # )
    # proc_engine = subprocess.Popen(
    #     ['python', '-m', 'salver.controller.app'], preexec_fn=os.setsid, env=env
    # )

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    agent = Process(target=start_agent)
    controller = Process(target=start_controller)

    agent.start()
    controller.start()

    def wait_for_engine():
        while True:
            time.sleep(1)
            print("SALUT")
            if tasks.ping.delay().get():
                print("UP")
                tasks.reload_agents.delay().get()
                return boot()

    # request.addfinalizer(lambda: os.killpg(os.getpgid(proc_agent.pid), signal.SIGKILL))
    # request.addfinalizer(lambda: os.killpg(os.getpgid(proc_engine.pid), signal.SIGKILL))
    request.addfinalizer(lambda: agent.terminate())
    request.addfinalizer(lambda: controller.terminate())
    wait_for_engine()
