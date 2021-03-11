
from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.domain import Domain


class Kupa3(DockerCollector):
    config = {
        "name": "kupa3",
        "docker": {
            "build_context": get_actual_dir(),
        },
    }

    def callbacks(self):
        return {
            Domain: self.scan
	}

    def scan(self, domain):
        data = self.run_container(command=["ls", "-la"])
        for item in self.findall_regex(data, r"(.*)"):
            yield



