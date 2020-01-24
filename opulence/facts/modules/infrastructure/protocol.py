from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Protocol(BaseFact):
    _name_ = "Protocol"
    _description_ = "Represent a protocol"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.name = StringField(mandatory=True, default="ssh")
        self.id = StringField()

    def get_summary(self):
        return "{}".format(self.name.value)
