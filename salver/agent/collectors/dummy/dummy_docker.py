# -*- coding: utf-8 -*-
from salver.common.facts import Email, Username
from salver.common.limiter import Duration, RequestRate
from salver.agent.collectors import DockerCollector
from salver.common.utils import get_actual_dir


class Dummy(DockerCollector):
    config = {
        "name": "dummy-docker-collector",
        "limiter": [RequestRate(limit=1, interval=Duration.SECOND)],
        "docker": {
            "build_context": get_actual_dir()
        }
    }

    def callbacks(self):
        return {
            Email: self.cb_email, 
            Username: self.cb_username,
        }

    def cb_username(self, username):
        whoami = self.run_container(command="whoami")
        yield Username(name= username.name + whoami)
        yield Email(address="dummy@" + whoami)

    def cb_email(self, email):
        date = self.run_container(command="date")
        yield Username(name=email.address + date)
        yield Email(address="dummy@" + date)
