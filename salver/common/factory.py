# -*- coding: utf-8 -*-
import os
import sys
import inspect
import pkgutil
import traceback
from abc import ABC, abstractmethod
from importlib import import_module

from loguru import logger

from salver.common.singleton import Singleton


class Factory(ABC, Singleton):
    @property
    def items(self):
        if hasattr(self, "_items"):
            return self._items
        return None

    @items.setter
    def items(self, items):
        self._items = items

    @abstractmethod
    def build(self):
        pass

    @staticmethod
    def _discover_packages(path):
        for (_, name, ispkg) in pkgutil.iter_modules([path]):
            pkg_path = os.path.join(path, name)
            if ispkg:
                yield from Factory._discover_packages(pkg_path)
                continue
            if pkg_path.startswith("./"):
                pkg_path = pkg_path[2:]
            yield pkg_path.replace("/", ".")

    @staticmethod
    def load_classes_from_module(root_path, parent_class):
        modules = []
        for mod_path in Factory._discover_packages(root_path):
            module = None
            if mod_path not in sys.modules:
                try:

                    module = import_module(mod_path)
                except Exception as err:
                    traceback.print_exc(file=sys.stdout)
                    logger.critical(f"Could not import module {mod_path}: {err}")

            else:
                module = sys.modules[mod_path]
            for _, mod_cls in inspect.getmembers(module, inspect.isclass):
                if (
                    mod_cls.__module__.startswith(mod_path)
                    and issubclass(mod_cls, parent_class)
                    and parent_class != mod_cls
                ):
                    modules.append(mod_cls)
        return modules
