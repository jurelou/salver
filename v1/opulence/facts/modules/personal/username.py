from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Username(BaseFact):
    _name_ = "Username"
    _description_ = "Represent an online username"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.name = StringField(mandatory=True, default="JohnSnow")

    def get_summary(self):
        return f"{self.name.value}"
