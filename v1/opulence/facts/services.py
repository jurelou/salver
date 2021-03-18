# -*- coding: utf-8 -*-
from importlib import import_module

from opulence.engine.database import DataWriter


def fact_from_json(json_obj):
    for f in DataWriter().facts.get():
        print("GHO")
        if f.external_identifier == json_obj["input_type"]:
            splitted_path = f.plugin_data["canonical_name"].split(".")
            module = import_module(".".join(splitted_path[:-1]))
            fact_cls = getattr(module, splitted_path[-1])
            fact = fact_cls(**json_obj["fields"])
            return fact if fact.is_valid() else None
    return None


def facts_from_json(json_list):
    result = [fact_from_json(i) for i in json_list]
    return list(filter(None, result))
