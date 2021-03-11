import importlib

from opulence.common.plugins.exceptions import PluginFormatError

from .baseCollector import BaseCollector


class PypiCollector(BaseCollector):
    _modules_ = {}
    modules = {}

    def __init__(self, *args, **kwargs):
        if not self._modules_:
            raise PluginFormatError("No modules provided")
        if not isinstance(self._modules_, dict):
            raise PluginFormatError("Modules should be of type `dict`")
        for key, value in self._modules_.items():
            self.modules[key] = importlib.import_module(value)
        super().__init__()

    @property
    def plugin_category(self):
        return PypiCollector.__name__
