# -*- coding: utf-8 -*-
from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.email import Email
from opulence.facts.person import Person


class DummyDocker(DockerCollector):
    config = {
        "name": "dummy-docker-collector",
        "docker": {
            "build_context": get_actual_dir(),
        },
    }

    def callbacks(self):
        return {
            Person: self.cb_person,
            Email: self.cb_email,
        }

    def cb_person(self, person):
        whoami = self.run_container(command="whoami")
        yield Person(firstname="dummy docker", lastname=whoami)
        yield Email(address="dummy@email")

    def cb_email(self, email):
        date = self.run_container(command="date")
        yield Person(firstname="dummy docker", lastname=date)
        yield Email(address="dummy@email")
