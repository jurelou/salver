import json

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import CPE
from opulence.facts import URI


class Wappalyzer(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "wappalyzer"
    _description_ = "Uncovers technologies used on websites"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("wappalyzer")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = URI

    ###############
    # Script attributes
    ###############
    _script_path_ = "wappalyzer"
    _script_arguments_ = ["$URI.full_uri$"]

    def parse_result(self, result):
        result = json.loads(result)
        for app in result["applications"]:
            yield CPE(
                id=app["cpe"],
                confidence=app["confidence"],
                name=app["name"],
                version=app["version"],
                website=app["website"],
            )
