from opulence.common.fields import BooleanField, StringField
from opulence.facts.bases import BaseFact


class CryptoKey(BaseFact):
    _name_ = "CryptoKey"
    _description_ = "Represent an asymmetric cryptography key"
    _author_ = "Henry"
    _version_ = 1

    def setup(self):
        self.key = StringField(mandatory=True)
        self.categorie = StringField()
        self.private = BooleanField(default=True)

    def get_summary(self):
        return f"{self.key.value}"
