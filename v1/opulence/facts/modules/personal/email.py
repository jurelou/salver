from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Email(BaseFact):
    _name_ = "Email"
    _description_ = "Represent an email address"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.address = StringField(mandatory=True, default="john@example.com")

    def get_summary(self):
        return f"{self.address.value}"
