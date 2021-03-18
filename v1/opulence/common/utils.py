# -*- coding: utf-8 -*-
from datetime import datetime
import uuid

from dateutil.parser import parse


def now():
    return datetime.now()


def datetime_to_str(date: datetime):
    if isinstance(date, datetime):
        return date.isoformat()
    return None


def str_to_datetime(s: str):
    if s is not None:
        return parse(s)
    return None


def hex_to_uuid(hex):
    return uuid.UUID(hex)


def generate_uuid():
    return uuid.uuid4()


def is_iterable(element):
    try:
        iter(element)
    except TypeError:
        return False
    else:
        return True


def is_list(element):
    return isinstance(element, (set, list, tuple))


def replace_dict_keys(d, convert_function):
    new = {}
    for k, v in d.items():
        new_v = v
        if isinstance(v, dict):
            new_v = replace_dict_keys(v, convert_function)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                new_v.append(replace_dict_keys(x, convert_function))
        new[convert_function(k)] = new_v
    return new
