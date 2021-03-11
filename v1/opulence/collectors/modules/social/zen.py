import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.passwordstore import Store
from opulence.common.plugins.dependencies import (
    BinaryDependency, PasswordDependency
)
from opulence.facts import Email, GitRepository, Organization, Username


class Zen(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Zen"
    _description_ = "Find email addresses of Github users."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("zen"), PasswordDependency("github_user")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (Organization, Username, GitRepository)
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "zen"

    def launch(self, fact):
        cmd = [self._script_path_, "-u", Store().get_decrypted_password("github_user")]
        if isinstance(fact, Username):
            cmd.append(fact.name.value)
        elif isinstance(fact, GitRepository):
            url = (
                fact.url.value[:-4]
                if fact.url.value.endswith(".git")
                else fact.url.value
            )
            cmd.append(url)
        elif isinstance(fact, Organization):
            cmd.extend(["--org", fact.name.value])
        yield from self.parse_result(self._exec(*cmd))

    @staticmethod
    def parse_result(result):
        res = re.findall("(.*) : (.*)", result)
        if res:
            for r in res:
                username, email = r
                yield Username(name=username)
                yield Email(address=email)
