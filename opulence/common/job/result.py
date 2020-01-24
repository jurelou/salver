from opulence.facts.bases import BaseFact
from opulence.facts.bases.utils import is_fact_or_composite

from ..patterns import Composite, JsonSerializable, is_composite
from ..timer import Clock
from ..utils import generate_uuid, hex_to_uuid, is_list
from .status import StatusCode


class Composable(JsonSerializable):
    def __init__(self, data=None):
        self.data = data

    @property
    def data(self):
        return self._data

    def __eq__(self, other):
        if not isinstance(other, Composable):
            return False
        s_items = self.get(force_array=True)
        o_items = other.get(force_array=True)
        for s, o in zip(s_items, o_items):
            if s != o:
                return False
        return True

    @data.setter
    def data(self, data):
        if is_fact_or_composite(data):
            self._data = data
        else:
            self._data = None

    def get(self, force_array=False):
        if is_composite(self.data):
            return self.data.elements
        if force_array:
            return [] if not self.data else [self.data]
        else:
            return self.data


class Result(JsonSerializable):
    def __init__(
        self,
        input=None,
        output=None,
        status=StatusCode.undefined,
        identifier=None,
        clock=None,
        collector_data=None,
    ):
        if identifier is None:
            self.identifier = generate_uuid()
        else:
            self.identifier = identifier

        if clock is None:
            self.clock = Clock()
        else:
            self.clock = clock

        self.input = input
        self.output = output
        self.status = status
        self.collector_data = collector_data

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        self._input = Composable(input)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        self._output = output if (is_list(output) or output is None) else [output]

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        try:
            statusCode, error = status
        except TypeError:
            self._status = {
                "status": status,
                "code": StatusCode.code_to_label(status),
                "error": None,
            }
        else:
            self._status = {
                "status": statusCode,
                "code": StatusCode.code_to_label(statusCode),
                "error": error,
            }

    def get_info(self):
        input = self.input.get()
        input_json = None
        if is_list(input):
            input_json = [i.get_info() for i in input]
        elif input is not None:
            input_json = [input.get_info()]

        output_json = []
        if self.output:
            output_json = [out.get_info() for out in self.output]

        obj_dict = {
            "input": input_json,
            "output": output_json,
            "clock": self.clock.to_json(),
            "identifier": self.identifier.hex,
            "collector": self.collector_data,
            "status": (int(self.status["status"]), self.status["error"]),
        }
        return obj_dict

    def to_json(self):
        input = self.input.get()
        input_json = []
        if is_list(input):
            input_json = [i.to_json() for i in input]
        elif input:
            input_json = input.to_json()

        output_json = []
        if self.output:
            output_json = [out.to_json() for out in self.output]

        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            "identifier": self.identifier.hex,
            "collector_data": self.collector_data,
            "input": input_json,
            "output": output_json,
            "clock": self.clock.to_json(),
            "status": (int(self.status["status"]), self.status["error"]),
        }
        return obj_dict

    @staticmethod
    def from_json(json_dict):
        if is_list(json_dict["input"]):
            input_list = [BaseFact.from_json(i) for i in json_dict["input"]]
            input_cls = Composite(input_list)
        else:
            input_cls = BaseFact.from_json(json_dict["input"])

        output = []
        if "output" in json_dict and json_dict["output"]:
            output = [BaseFact.from_json(o) for o in json_dict["output"]]

        json_dict.update(
            {
                "output": output,
                "input": input_cls,
                "identifier": hex_to_uuid(json_dict["identifier"]),
                "clock": Clock.from_json(json_dict["clock"]),
            }
        )
        return super(Result, Result).from_json(json_dict)
