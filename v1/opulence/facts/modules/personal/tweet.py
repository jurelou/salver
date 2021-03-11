from opulence.common.fields import IntegerField
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Tweet(BaseFact):
    _name_ = "Port"
    _description_ = "Represent a tweet from twitter."
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.id = IntegerField(mandatory=True)
        self.message = StringField(mandatory=True)
        self.author = StringField(mandatory=True)
        self.date = StringField(mandatory=True)  # DateField ?

    def get_summary(self):
        return f"{self.message.value}"
