#!/bin/bash

lower_name=$(echo "$1" | awk '{print tolower($0)}')
collector_dir="./opulence/agent/collectors/$lower_name"

mkdir $collector_dir
touch $collector_dir/__init__.py
cat > $collector_dir/Dockerfile << EOL
FROM python:3.6-buster

WORKDIR /$1

RUN git clone --depth 1 --branch ... https://github.com/.. /$1 \\
	&& cd /$1 \\
	&& pip3 install -r requirements.txt

ENTRYPOINT [ "python", "..." ]

EOL

cat > $collector_dir/collector.py << EOL

from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.domain import Domain


class $1(DockerCollector):
    config = {
        "name": "$lower_name",
        "docker": {
            "build_context": get_actual_dir(),
        },
    }

    def callbacks(self):
        return {
            Email: self.scan
	}

    def scan(self, domain):
        data = self.run_container(command="ls", "-la")
        for item in self.findall_regex(data, r"(.*)"):
            yield 



EOL

echo "Done $lower_name"


