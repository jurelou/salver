from opulence.common.fields import IntegerField
from opulence.facts.bases import BaseFact


class TravelTime(BaseFact):
    _name_ = "travelTime"
    _description_ = "Represent a duration, departure, arrival time"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.scheduled_arrival = IntegerField()
        self.scheduled_departure = IntegerField()
        self.real_arrival = IntegerField()
        self.real_departure = IntegerField()
        self.duration = IntegerField()

    def get_summary(self):
        return f"{self.duration.value}"
