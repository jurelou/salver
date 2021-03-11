from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Person(BaseFact):
    _name_ = "Person"
    _description_ = "Represent a person firstname and lastname"
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.lastname = StringField(mandatory=True, default="John")
        self.firstname = StringField(mandatory=True, default="Snow")

    def get_summary(self):
        return "{} {}".format(self.firstname.value, self.lastname.value)
