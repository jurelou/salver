import re

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins.dependencies import BinaryDependency
from opulence.facts import Tweet
from opulence.facts import Username


class Twint(ScriptCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "twint"
    _description_ = "Gather information from a user's twitter profile."
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [BinaryDependency("twint")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = Username
    _active_scanning_ = False

    ###############
    # Script attributes
    ###############
    _script_path_ = "twint"

    def launch(self, fact):
        gather_tweets = [self._script_path_, "-u", fact.name.value]
        gather_favorites = [self._script_path_, "-u", fact.name.value, "--favorites"]
        gather_followers = [self._script_path_, "-u", fact.name.value, "--followers"]
        gather_following = [self._script_path_, "-u", fact.name.value, "--following"]

        yield from self.parse_tweets(self._exec(*gather_tweets))
        yield from self.parse_tweets(self._exec(*gather_favorites))
        yield from self.parse_usernames(self._exec(*gather_followers))
        yield from self.parse_usernames(self._exec(*gather_following))

    @staticmethod
    def parse_tweets(stdout):
        found_tweets = re.findall(
            "(\\d{15,21}) ([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]) (?:(?:[01]?\\d|2[0-3]:)?[0-5]?\\d:)?[0-5]?\\d) (.*) <(.*)> (.*)",  # noqa: E501
            stdout,
        )
        if found_tweets:
            for f in found_tweets:
                t_id, date, _, _, tz, username, message = f
                yield Tweet(id=t_id, message=message, author=username, date=date)

    @staticmethod
    def parse_usernames(stdout):
        followers = stdout.split("\n")
        if followers:
            for name in followers:
                if name and not name.startswith("CRITICAL:"):
                    yield Username(name=name)
