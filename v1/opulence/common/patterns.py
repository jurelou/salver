import importlib

from .utils import is_list


class JsonSerializable:
    def to_json(self):
        dict_whithout_private = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
        obj_dict = {"__class__": self.__class__.__name__, "__module__": self.__module__}
        obj_dict.update(dict_whithout_private)
        return obj_dict

    @staticmethod
    def from_json(json_dict):
        if "__class__" in json_dict:
            class_name = json_dict.pop("__class__")
            module_name = json_dict.pop("__module__")

            module = importlib.import_module(module_name)
            _class = getattr(module, class_name)
            obj = _class(**json_dict)
        else:  # pragma: no cover
            obj = json_dict
        return obj


class Composite(JsonSerializable):
    def __init__(self, *args):
        self._elements = []
        for a in args:
            if is_list(a):
                self._elements.extend(a)
            else:
                self._elements.append(a)

    @property
    def elements(self):
        return self._elements


def is_composite(obj):
    return isinstance(obj, Composite)


class SingletonMetaClass(type):
    _instances_ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances_:
            cls._instances_[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs
            )
        return cls._instances_[cls]


Singleton = SingletonMetaClass("Singleton", (object,), {})
