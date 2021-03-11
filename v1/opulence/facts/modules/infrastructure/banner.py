from opulence.common.fields import IntegerField
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Banner(BaseFact):
    _name_ = "Banner"
    _description_ = r"""
        Banners are usually text messages displayed by a service.
        Banners usually contain information about a service, such as the version number.
        """
    _author_ = "Louis"
    _version_ = 1

    def setup(self):
        self.message = StringField(mandatory=True, default="Hello world")
        self.port = IntegerField()
        self.product = StringField()

    def get_summary(self):
        return f"{self.message.value}"
