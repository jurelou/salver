# -*- coding: utf-8 -*-
import re

from salver.agent.collectors.docker import DockerCollector
from salver.common.utils import get_actual_dir
from salver.facts import Domain
from salver.facts import Person
from salver.facts import Uri


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
