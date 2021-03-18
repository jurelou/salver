from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.email import Email
from opulence.facts.person import Person


class DummyDocker(DockerCollector):
    config = {
        "name": "dummy-docker-collector",
        "docker": {
            # "image": "ubuntu:latest"
            "build_context": get_actual_dir(),
        },
        # "periodic": True,
        # "schedule": {
        #     "minute": "*"
        # }
    }

    def callbacks(self):
        return {
            Person: self.cb_person,
            Email: self.cb_email
        }

    def cb_person(self, person):
        hello = self.run_container(command="whoami")
        yield Person(firstname="dummy docker from person", lastname=hello)
        yield Email(address="yes from person")

    def cb_email(self, email):
        hello = self.run_container(command="whoami")
        yield Person(firstname="dummy docker from email", lastname=hello)
        yield Email(address="yes from email")
