import opulence.facts as facts
from opulence.collectors.bases import PypiCollector
from opulence.common.passwordstore import Store
from opulence.common.plugins.dependencies import ModuleDependency, PasswordDependency


class Censys(PypiCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Censys"
    _description_ = "Gather information about a domain using censys"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [
        ModuleDependency("censys"),
        PasswordDependency("censys_api_id"),
        PasswordDependency("censys_secret"),
    ]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = facts.IPv4
    _active_scanning_ = False

    ###############
    # Pypi attributes
    ###############
    _modules_ = {"censys": "censys.ipv4"}

    _api_id_ = Store().get_decrypted_password("censys_api_id")
    _api_key_ = Store().get_decrypted_password("censys_secret")

    def launch(self, fact):
        api = self.modules["censys"].CensysIPv4(
            api_id=self._api_id_, api_secret=self._api_key_,
        )

        result = api.view(fact.address.value)

        yield facts.ASN(
            id=result["autonomous_system"]["asn"],
            prefix=result["autonomous_system"]["routed_prefix"],
            organization=result["autonomous_system"]["name"],
            rir=result["autonomous_system"]["rir"],
        )

        yield facts.Country(
            name=result["location"]["country"],
            code=result["location"]["country_code"],
            timezone=result["location"]["timezone"],
            continent=result["location"]["continent"],
        )

        yield facts.GeoCoordinates(
            longitude=result["location"]["longitude"],
            latitude=result["location"]["latitude"],
        )

        # ports = result["ports"]
        # TODO: do something with this
