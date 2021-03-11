import re

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.domain import Domain
from opulence.facts.person import Person


class DummyDocker(DockerCollector):
    config = {
        "name": "recon-ng",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {Domain: self.from_domain}

    def run_hacker_target(self, fqdn):
        yield
        data = self.run_container(
            command=[
                "-m",
                "recon/domains-hosts/hackertarget",
                "-o",
                f"SOURCE={fqdn}",
                "-x",
            ],
        )
        for item in self.findall_regex(data, r"Host: (.*)"):
            yield Domain(fqdn=item)

    def from_domain(self, domain):
        yield from self.run_hacker_target(domain.fqdn)
        # hello = self.run_container(command="whoami")
        # print("exec docker collector")
        # yield Person(firstname="dummy docker collector", lastname=hello)
        # yield Email(address="yes")
