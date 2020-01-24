from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Plane(BaseFact):
    _name_ = "Plane"
    _description_ = "Represent a plane model"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.name = StringField(mandatory=True)
        self.code = StringField()

    def get_summary(self):
        return "{}".format(self.name.value)
