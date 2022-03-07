from datetime import datetime
import inspect
import os

def get_actual_dir():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    return os.path.dirname(os.path.abspath(module.__file__))

def datetime_to_str(date: datetime):
    return date.isoformat()


def str_to_datetime(s: str):
    return parse(s)


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
