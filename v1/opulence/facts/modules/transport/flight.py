from opulence.common.fields import BooleanField, StringField
from opulence.facts.bases import BaseFact


class Flight(BaseFact):
    _name_ = "Flight"
    _description_ = "Represent a Flight with his number"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.flight_number = StringField(mandatory=True, default="AF1124")
        self.status = StringField()
        self.type = StringField()
        self.live = BooleanField()

    def get_summary(self):
        return f"{self.flight_number.value}"
