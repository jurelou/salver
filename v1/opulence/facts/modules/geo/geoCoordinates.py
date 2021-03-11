from opulence.common.fields import FloatField
from opulence.facts.bases import BaseFact


class GeoCoordinates(BaseFact):
    _name_ = "GeoCoordinates"
    _description_ = "GPS coordinates (latitude / longitude)"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.latitude = FloatField(mandatory=True, default=42)
        self.longitude = FloatField(mandatory=True, default=42)

    def get_summary(self):
        return "{} {}".format(self.latitude.value, self.longitude.value)
