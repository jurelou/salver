from opulence.common.fields import IntegerField, StringField
from opulence.facts.bases import BaseFact


class VulDB(BaseFact):
    _name_ = "VulDB"
    _description_ = "VULDB vulnerability identifier"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.id = IntegerField(mandatory=True, default=133852)
        self.description = StringField()

    def get_summary(self):
        return f"{self.id.value}"
