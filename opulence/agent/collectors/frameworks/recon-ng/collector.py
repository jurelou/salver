import re

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.domain import Domain
from opulence.facts.person import Person
from opulence.facts.profile import Profile
from opulence.facts.username import Username


class DummyDocker(DockerCollector):
    config = {
        "name": "recon-ng",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {
            Domain: self.from_domain,
            Username: self.from_username,
        }

    def from_domain(self, domain):
        data = self.run_container(
            command=[
                "-m",
                "recon/domains-hosts/hackertarget",
                "-o",
                f"SOURCE={domain.fqdn}",
                "-x",
            ],
        )
        for item in self.findall_regex(data, r"Host: (.*)"):
            yield Domain(fqdn=item)

    def from_username(self, username):
        data = self.run_container(
            command=["-m", "profiler", "-o", f"SOURCE={username.name}", "-x",],
        )
        for category, resource, url in self.findall_regex(
            data, r"Category: (.*)\n.*\n.*Resource: (.*)\n.*Url: (.*)"
        ):
            yield Profile(url=url, category=category, resource=resource)
