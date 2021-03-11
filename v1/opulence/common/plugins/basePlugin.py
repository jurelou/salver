import inspect
import os
import pkgutil
import sys
from enum import IntEnum
from importlib import import_module

from ..patterns import Singleton
from ..utils import generate_uuid
from .exceptions import DependencyMissing, PluginVerifyError


class PluginStatus(IntEnum):
    UNDEFINED = 0
    READY = 10
    ERROR = 100

    def __ge__(self, other):
        return self.value >= other.value


class BasePlugin:
    _name_ = ""
    _description_ = ""
    _author_ = ""
    _version_ = ""
    _dependencies_ = ()
    _category_ = "Undefined"

    # internal use only
    _register_ = True
    _status_ = (PluginStatus.READY, "")

    def __init__(self):
        if not self._name_:
            self._name_ = "UNDEFINED-%s" % (generate_uuid())
            self.status = (
                PluginStatus.ERROR,
                "PluginFormatError: Incorrect plugin_name",
            )
        if not self._description_:
            self.status = (
                PluginStatus.ERROR,
                "PluginFormatError: Incorrect plugin_description",
            )
        if not self._author_:
            self.status = (
                PluginStatus.ERROR,
                "PluginFormatError: Incorrect plugin_author",
            )
        if not self._version_:
            self.status = (
                PluginStatus.ERROR,
                "PluginFormatError: Incorrect plugin_version",
            )
        if self._register_:
            PluginManager().register_plugin(self)

    @property
    def plugin_category(self):
        return BasePlugin.__name__

    @property
    def status(self):
        return self._status_

    @status.setter
    def status(self, code):
        try:
            code, error = code
        except TypeError:
            self._status_ = (PluginStatus.ERROR, "Wrong status arguments.")
        else:
            err_text = "" if error is None else error
            full_error = (
                "{}; {}".format(self._status_[1], {err_text})
                if self._status_[1] != ""
                else err_text
            )
            self._status_ = (code, full_error)

    @property
    def plugin_name(self):
        return self._name_

    @property
    def plugin_description(self):
        return self._description_

    @property
    def plugin_author(self):
        return self._author_

    @property
    def plugin_version(self):
        return self._version_

    @property
    def plugin_dependencies(self):
        return self._dependencies_

    @property
    def plugin_canonical_name(self):
        return ".".join([self.__module__, self.__class__.__name__])

    @property
    def errored(self):
        return self.status[0] >= PluginStatus.ERROR

    def get_info(self):
        return {
            "plugin_data": {
                "name": self.plugin_name,
                "version": str(self.plugin_version),
                "author": self.plugin_author,
                "category": self.plugin_category,
                "description": self.plugin_description,
                "status": self.status[0],
                "error": self.status[1],
                "canonical_name": self.plugin_canonical_name,
            }
        }


class PluginManager(Singleton):
    _plugins_ = {}

    def get_plugins(self, package=None, instance=True):
        if package:
            instances = [
                self._plugins_[plugin]
                for plugin in self._plugins_
                if plugin.startswith(package)
            ]
        else:
            instances = list(self._plugins_.values())
        return [plugin if instance else type(plugin) for plugin in instances]

    def _load_plugin(self, module, path):
        for clsmember in inspect.getmembers(module, inspect.isclass):
            if issubclass(clsmember[1], BasePlugin) and clsmember[
                1
            ].__module__.startswith(path):
                clsmember[1]()

    def _import_module(self, plugin):
        try:
            module = import_module(plugin)
        except ModuleNotFoundError as err:
            print("Module not found ({}): {}".format(plugin, err))
        except Exception as err:
            print("Import module failed: {}".format(err))
        else:
            return module
        return None

    def discover(self, path=None):
        if path is None:
            path = os.path.dirname(__file__)
        fs_path = path.replace(".", "/")
        for (_, name, ispkg) in pkgutil.iter_modules([fs_path]):
            pkg_name = "{}.{}".format(path, name)
            if pkg_name not in sys.modules:
                module = self._import_module(pkg_name)
            else:
                module = sys.modules[pkg_name]
            if module is not None:
                self._load_plugin(module, path)
            if ispkg:
                self.discover(pkg_name)

    def register_plugin(self, plugin):
        for dependency in plugin.plugin_dependencies:
            try:
                dependency.verify()
            except DependencyMissing as err:
                plugin.status = (PluginStatus.ERROR, str(err))
        if hasattr(plugin, "verify"):
            try:
                plugin.verify()
            except PluginVerifyError as err:
                plugin.status = (PluginStatus.ERROR, str(err))
        if plugin.plugin_canonical_name not in self._plugins_:
            self._plugins_[plugin.plugin_canonical_name] = plugin
