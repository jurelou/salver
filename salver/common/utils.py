# -*- coding: utf-8 -*-
import os
import inspect
import operator
import functools
import itertools

from loguru import logger


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


def is_list(element):
    """Check if item is a list."""
    return isinstance(element, (set, list, tuple))


def make_flat_list(data):
    """Convert any iterable to a flat list, recursively."""
    if not is_iterable(data):
        return [data]
    res = []
    for item in data:
        if not item:
            continue
        if is_list(item):
            res.extend(item)
        else:
            res.append(item)
    return res
