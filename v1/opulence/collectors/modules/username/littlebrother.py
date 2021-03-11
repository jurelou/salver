import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import URI, Email, Username


class LittleBrother(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "LittleBrother"
    _description_ = "Find online presence."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("LittleBrother")]

    ###############
    # Collector attributes
    ###############
    _active_scanning_ = False
    _allowed_input_ = (Email, Username)

    ###############
    # Script attributes
    ###############
    _script_path_ = "LittleBrother"

    def launch(self, fact):
        command = [self._script_path_]
        if isinstance(fact, Username):
            stdin = [
                f"1\n2\n{fact.name.value}\n",
                f"1\n10\n{fact.name.value}\n",
            ]
        elif isinstance(fact, Email):
            stdin = [f"1\n10\n{fact.address.value}\n"]

        for i in stdin:
            yield from self.parse_result(
                self._exec(*command, stdin=i, ignore_error=True),
            )

    def parse_result(self, result):
        urls = re.findall("\\[\\+\\] Possible connection: (.*)\\n", result)
        if urls:
            for url in urls:
                yield URI(full_uri=url)
