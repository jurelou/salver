import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain


class HackerTarget(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Hacker target"
    _description_ = "Uses the HackerTarget.com API to find host names."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("recon-ng")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "recon-ng"
    _script_arguments_ = [
        "-m",
        "recon/domains-hosts/hackertarget",
        "-o",
        "SOURCE=$Domain.fqdn$",
        "-x",
    ]

    def parse_result(self, result):
        results = []
        found_domains = re.findall("(.*)\\[host\\] (.*) \\((.*)\\)", result)

        if not found_domains:
            return results
        for f in found_domains:
            _, domain, url = f
            results.append(Domain(fqdn=domain))
        return results
