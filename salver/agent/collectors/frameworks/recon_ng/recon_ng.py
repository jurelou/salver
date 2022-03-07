# -*- coding: utf-8 -*-
from loguru import logger

from salver.common.facts import Domain, Person, OnlineProfile, Username
from salver.common.utils import get_actual_dir
from salver.agent.collectors import DockerCollector


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
        logger.debug(data)
        for item in self.findall_regex(data, r"Host: (.*)"):
            yield Domain(fqdn=item)

    def from_username(self, username):
        data = self.run_container(
            command=["-m", "profiler", "-o", f"SOURCE={username.name}", "-x"],
        )
        logger.debug(data)
        for category, resource, url in self.findall_regex(
            data,
            r"Category: (.*)\n.*\n.*Resource: (.*)\n.*Url: (.*)",
        ):
            yield OnlineProfile(url=url, category=category, resource=resource)