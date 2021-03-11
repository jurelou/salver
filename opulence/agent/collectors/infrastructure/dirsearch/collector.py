import re

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.domain import Domain
from opulence.facts.person import Person
from opulence.facts.uri import Uri


class Dirsearch(DockerCollector):
    config = {
        "name": "dirsearch",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {Domain: self.from_domain}

    def from_domain(self, domain):
        data = self.run_container(
            command=["-u", domain.fqdn, "-F", "--timeout=5", "-q", "-t", "4"],
        )
        print("!!!!", data)

        for item in self.findall_regex(data, r"2\d\d - .* - ([^\s]+)"):
            yield Uri(location=item)
