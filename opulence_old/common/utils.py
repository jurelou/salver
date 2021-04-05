# -*- coding: utf-8 -*-
from importlib import import_module
import inspect
import os
import pkgutil
import sys


def get_actual_dir():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    return os.path.dirname(os.path.abspath(module.__file__))


def is_iterable(element):
    try:
        iter(element)
    except TypeError:
        return False
    else:
        return True


def is_list(element):
    return isinstance(element, (set, list, tuple))


def make_list(data):
    if is_iterable(data):
        return list(data)
    if not is_list(data):
        return [data]
    return data
