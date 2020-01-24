from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Phone(BaseFact):
    _name_ = "Phone"
    _description_ = "Represent a phone number"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.number = StringField(mandatory=True, default="+33 6 42 42 42 42")
        self.carrier = StringField()
        self.localformat = StringField()
        self.line_type = StringField()

        self.country_code = StringField()
        self.city_code = StringField()
        self.area_code = StringField()
        self.rest = StringField()

    def get_summary(self):
        return "{}".format(self.number.value)
