from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain


class Sublister(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Sublist3r"
    _description_ = "DNS subdomains enumeration using sublist3r."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("sublist3r")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain

    ###############
    # Script attributes
    ###############
    _script_path_ = "sublist3r"
    _script_arguments_ = ["--domain", "$Domain.fqdn$"]

    def parse_result(self, result):
        res = result.split("Total Unique Subdomains")[1]
        if res:
            domains = res.split("\n")
            for domain in domains[1:]:
                yield Domain(fqdn=domain[5:-4])
