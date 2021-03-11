import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain, IPv4, Waf


class WafWoof(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "WafW00f"
    _description_ = "Detect if a website is using a WAF"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("wafw00f")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (Domain, IPv4)
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "wafw00f"

    def launch(self, fact):
        if isinstance(fact, Domain):
            commands = [
                [self._script_path_, "http://{}".format(fact.fqdn.value)],
                [self._script_path_, "https://{}".format(fact.fqdn.value)],
            ]
        elif isinstance(fact, IPv4):
            commands = [
                [self._script_path_, "http://{}".format(fact.address.value)],
                [self._script_path_, "https://{}".format(fact.address.value)],
            ]
        for command in commands:
            yield from self.parse_result(self._exec(*command))

    def parse_result(self, result):
        found_waf = re.findall("is behind *(.*?) \\(?(.*?)\\)? *WAF.", result)
        if found_waf:
            for f in found_waf:
                try:
                    name, vendor = f
                    yield Waf(name=name, vendor=vendor)
                except Exception:
                    yield Waf(name=f)
