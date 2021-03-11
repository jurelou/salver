from opulence.collectors.bases import BaseCollector
from opulence.facts import Person


class Test(BaseCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "test"
    _description_ = "test"
    _author_ = "Louis"
    _version_ = 1

    ###############
    # Module attributes
    ###############
    _allowed_input_ = Person

    def launch(self, facts):
        return Person(firstname=f"TEST-{facts.firstname.value}", lastname=f"TEST-")
