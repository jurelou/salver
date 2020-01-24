from ..patterns import JsonSerializable


class BaseField(JsonSerializable):
    def __init__(self, value=None, default=None, mandatory=False):
        self.default = default
        self._mandatory = mandatory
        self._value = None
        self.value = value
        self._modified = False

    def __repr__(self):
        return "{}  -> value: {}, default: {}, mandatory: {}".format(
            self.__class__.__name__, self.value, self._default, self._mandatory
        )

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

    @property
    def mandatory(self):
        return self._mandatory

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default):
        if default is not None:
            self._default = self.cast_value(default)
        else:
            self._default = None

    @property
    def value(self):
        if self._value is not None:
            return self._value
        return self.default

    @value.setter
    def value(self, value):
        if value is not None:
            self._modified = True
            self._value = self.cast_value(value)
        else:
            self._value = None

    def cast_value(self, value):
        return str(value)

    def to_json(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            "value": self.value,
            "default": self.default,
            "mandatory": self.mandatory,
        }
        return obj_dict
