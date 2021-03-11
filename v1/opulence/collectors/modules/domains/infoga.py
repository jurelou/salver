import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Domain
from opulence.facts import Email


class Infoga(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Infoga"
    _description_ = """
        Find emails from subdomains from public sources.
        seach engines, PGP key servers, shodan ..."""
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("infoga")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Domain
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "infoga"
    _script_arguments_ = ["--domain", "$Domain.fqdn$", "--breach"]

    def parse_result(self, result):
        emails = re.findall(" Email: *(.*?) *\\(*?\\)", result)
        if emails:
            for email in emails:
                yield Email(address=email)
