import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain


class Ctfr(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "ctfr"
    _description_ = "Subdomains enumaration using certificate transparency."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("ctfr")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "ctfr"
    _script_arguments_ = ["--domain", "$Domain.fqdn$"]

    def parse_result(self, result):
        found_domains = re.findall("\\[-\\] *(.*)", result)
        if found_domains:
            for f in found_domains:
                yield Domain(fqdn=f)
