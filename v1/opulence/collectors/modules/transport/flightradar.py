from opulence.collectors.bases import PypiCollector
from opulence.common.plugins.dependencies import ModuleDependency
from opulence.facts import Flight
from opulence.facts import GeoCoordinates
from opulence.facts import Plane
from opulence.facts import TravelTime


class FlightRadar(PypiCollector):
    ###############
    # Plugin attributes
    ###############
    _name_ = "Flight Radar"
    _description_ = "Return info about a Flight "
    _author_ = "Henry"
    _version_ = 1
    _dependencies_ = [ModuleDependency("flightradar24")]

    ###############
    # Module attributes
    ###############
    _allowed_input_ = Flight

    ###############
    # Pypi attributes
    ###############
    _modules_ = {"fr": "flightradar24"}

    __id = 0

    def airports_Parser(self, airports, type):
        latitude = airports["position"]["latitude"]
        longitude = airports["position"]["longitude"]
        return GeoCoordinates(
            latitude=latitude, longitude=longitude, type=type, id=self.__id,
        )

    def status_Parser(self, status, flight_number):
        return Flight(
            flight_number=flight_number,
            status=status["text"],
            type=status["generic"]["status"]["type"],
            live=status["live"],
            id=self.__id,
        )

    def time_Parser(self, time):
        duration = time["other"]["duration"]
        scheduled = time["scheduled"]
        if duration is None and scheduled["departure"] is not None:
            duration = scheduled["arrival"] - scheduled["departure"]
        return TravelTime(
            scheduled_arrival=scheduled["arrival"],
            scheduled_departure=scheduled["departure"],
            real_arrival=time["real"]["arrival"],
            real_departure=time["real"]["departure"],
            duration=duration,
            id=self.__id,
        )

    def plane_parser(self, plane):
        return Plane(name=plane["text"], code=plane["code"], id=self.__id)

    def parser(self, result, flight_number):
        data = result["response"]["data"]
        if data is None:
            return None
        for flight in data:
            self.__id = flight["identification"]["row"]
            yield self.airports_Parser(flight["airport"]["origin"], "origin")
            yield self.airports_Parser(flight["airport"]["destination"], "destination")
            yield self.status_Parser(flight["status"], flight_number)
            yield self.time_Parser(flight["time"])
            yield self.plane_parser(flight["aircraft"]["model"])

    def launch(self, facts):
        result = self.modules["fr"].Api().get_flight(facts.flight_number.value)
        yield from self.parser(result["result"], facts.flight_number.value)
