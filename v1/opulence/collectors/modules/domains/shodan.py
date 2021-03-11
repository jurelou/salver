import opulence.facts as facts
from opulence.collectors.bases import PypiCollector
from opulence.common.passwordstore import Store
from opulence.common.plugins.dependencies import ModuleDependency, PasswordDependency


class Shodan(PypiCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Shodan"
    _description_ = "Gather information aout a domain using shodan"
    _author_ = "Louis"
    _version_ = 1
    _dependencies_ = [ModuleDependency("shodan"), PasswordDependency("shodan_api")]

    ###############
    # Collector attributes
    ###############
    _allowed_input_ = (facts.IPv4, facts.IPv6)
    _active_scanning_ = False

    ###############
    # Pypi attributes
    ###############
    _modules_ = {"s": "shodan"}

    _apikey_ = Store().get_decrypted_password("shodan_api")

    def launch(self, fact):
        api = self.modules["s"].Shodan(self._apikey_)
        host = api.host(fact.address.value)

        yield facts.Country(
            name=host.get("country_name", None), code=host.get("country_code", None),
        )
        yield facts.Organization(name=host.get("org", None))
        yield facts.OperatingSystem(family=host.get("os", None))

        for item in host["data"]:
            if "cpe" in item:
                for cpe in item["cpe"]:
                    yield facts.CPE(id=cpe)
            if "os" in item:
                yield facts.OperatingSystem(family=item["os"])
            if "location" in item and "country_name" in item["location"]:
                yield facts.Country(
                    name=item["location"]["country_name"],
                    code=item["location"]["country_code"],
                )
            if (
                "location" in item
                and "longitude" in item["location"]
                and "latitude" in item["location"]
            ):
                yield facts.GeoCoordinates(
                    longitude=item["location"]["longitude"],
                    latitude=item["location"]["latitude"],
                )
            if "asn" in item:
                yield facts.ASN(id=item["asn"], organization=host.get("org", None))
            if "data" in item:
                yield facts.Banner(
                    message=item["data"],
                    port=host.get("port", None),
                    product=host.get("product", None),
                )
            if "port" in item:
                yield facts.Port(
                    number=item["port"], transport=host.get("transport", None),
                )
