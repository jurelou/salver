from opulence.agent.collectors.docker import DockerCollector
from opulence.common.utils import get_actual_dir
from opulence.facts.username import Username
from opulence.facts.tweet import Tweet


class Twint(DockerCollector):
    config = {
        "name": "twint",
        "docker": {"build_context": get_actual_dir(),},
    }

    def callbacks(self):
        return {Username: self.scan}

    def scan(self, username):
        regex = r"(\d+) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*<.*> (.*)"

        data = self.run_container(command=["-u", username.name, "--retweets"])
        for tweet_id, date, content in self.findall_regex(data, regex):
            yield Tweet(id=tweet_id, content=content, date=date, rt=True)

        data = self.run_container(command=["-u", username.name])
        for tweet_id, date, content in self.findall_regex(data, regex):
            yield Tweet(id=tweet_id, content=content, date=date, rt=False)