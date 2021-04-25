# -*- coding: utf-8 -*-
import os
import sys
import inspect
import pkgutil
import traceback
from abc import ABC, abstractmethod
from importlib import import_module


def get_actual_dir():
    """Get calling method absolute path."""
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    return os.path.dirname(os.path.abspath(module.__file__))


def is_iterable(element):
    """check if item is iterable."""
    try:
        iter(element)
    except TypeError:
        return False
    else:
        return True


def make_flat_list(data):
    """Convert any iterable to a flat list, recursively."""
    if not is_iterable(data):
        return [data]
    res = []
    for item in data:
        if not item:
            continue
        if isinstance(item, (set, list, tuple)):
            res.extend(item)
        else:
            res.append(item)
    return res


def _discover_packages(path):
    for (_, name, ispkg) in pkgutil.iter_modules([path]):
        pkg_path = os.path.join(path, name)
        if ispkg:
            yield from _discover_packages(pkg_path)
            continue
        if pkg_path.startswith('./'):
            pkg_path = pkg_path[2:]
        yield pkg_path.replace('/', '.')


def load_classes(root_path, parent_class):
    """Find all classes in a directory."""
    modules = []
    for mod_path in _discover_packages(root_path):
        module = None
        if mod_path not in sys.modules:
            try:
                module = import_module(mod_path)
            except Exception as err:
                traceback.print_exc(file=sys.stdout)
                logger.critical(f'Could not import module {mod_path}: {err}')
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


class Singleton:
    """Single instance class."""

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
