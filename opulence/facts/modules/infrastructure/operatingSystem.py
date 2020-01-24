from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class OperatingSystem(BaseFact):
    _name_ = "OperatingSystem"
    _description_ = "Represent an operating system name, version and vendor "
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.family = StringField(mandatory=True, default="Windows 10")
        self.vendor = StringField(mandatory=True, default="Microsoft")
        self.version = StringField()

    def get_summary(self):
        return "{}".format(self.family.value)
