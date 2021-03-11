import re

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.profile import Profile
from opulence.facts.username import Username


class Sherlock(DockerCollector):
    config = {
        "name": "sherlock",
        "docker": {"build_context": get_actual_dir()},
    }

    def callbacks(self):
        return {Username: self.from_username}

    def from_username(self, username):
        data = self.run_container(
            command=[username.name, "--no-color", "--print-found", "--timeout", "20"],
        )
        for item in self.findall_regex(data, r"\[\+\] .*: (.*)\n"):
            yield Profile(url=item)
