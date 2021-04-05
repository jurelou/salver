# -*- coding: utf-8 -*-
import re

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.domain import Domain
from opulence.facts.email import Email


class Infoga(DockerCollector):
    config = {
        "name": "infoga",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {Domain: self.scan}

    def scan(self, domain):
        data = self.run_container(command=["--domain", domain.fqdn, "-v", "1"])
        for item in self.findall_regex(data, r"Email: (.*) \("):
            yield Email(address=item)
