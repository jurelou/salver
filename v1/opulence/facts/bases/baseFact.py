from opulence.common.fields import BaseField, DynamicField
from opulence.common.patterns import JsonSerializable
from opulence.common.plugins.basePlugin import BasePlugin


class BaseFact(BasePlugin, JsonSerializable):
    def __init__(self, **kwargs):
        self.setup()
        for key, value in kwargs.items():
            if key in self.__dict__:
                if isinstance(value, BaseField):
                    self.__dict__[key] = value
                else:
                    self.__dict__[key].value = value
            else:
                setattr(self, key, DynamicField(value=value))
        self.summary = self.get_summary()
        super().__init__()

    def __hash__(self):
        val = 0
        for key, value in self.get_fields().items():
            val += hash(key) + hash(value)
        if val == 0:
            return -1
        return val

    def __eq__(self, other):
        return hash(self) == hash(other) if isinstance(other, BaseFact) else False

    def setup(self):
        pass

    def get_summary(self):
        return ""

    @property
    def plugin_canonical_name(self):
        return ".".join(["opulence.facts", self.__class__.__name__])

    @property
    def plugin_category(self):
        return ".".join(["fact"] + self.__module__.split(".")[3:-1])

    def is_valid(self):
        for _, f in self.get_fields().items():
            if f.mandatory is True and (f.value is f.default):
                return False
        return True

    def get_fields(self, json=False, summary=False):
        if not json:
            return {
                key: value
                for key, value in self.__dict__.items()
                if isinstance(value, BaseField)
            }

        if not summary:
            return {
                key: value.to_json()
                for key, value in self.__dict__.items()
                if isinstance(value, BaseField)
            }
        else:
            fields = {}
            for key, v in self.__dict__.items():
                if isinstance(v, BaseField):
                    fields[key] = {
                        "value": v.value,
                        "default": v.default,
                        "mandatory": v.mandatory,
                    }
            return fields

    def get_info(self):
        data = {
            "fields": self.get_fields(json=True, summary=True),
            "summary": self.summary,
        }
        return {**super().get_info(), **data}

    def to_json(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            "fields": self.get_fields(json=True),
        }
        return obj_dict

    @staticmethod
    def from_json(json_dict):
        fields = {
            key: BaseField.from_json(value)
            for key, value in json_dict["fields"].items()
        }
        del json_dict["fields"]
        json_dict.update(fields)
        return super(BaseFact, BaseFact).from_json(json_dict)
