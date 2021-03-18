# -*- coding: utf-8 -*-
import inspect

from opulence import App
from opulence.engine.database import DataWriter
import opulence.facts as all_facts
from opulence.facts.bases import BaseFact


@App.task(name="engine:facts.get")
def get():
    return DataWriter().facts.get().to_json()


@App.task(name="engine:facts.load")
def load():
    for m in inspect.getmembers(all_facts, inspect.isclass):
        fact_inst = m[1]()
        if isinstance(fact_inst, BaseFact):
            fact_info = fact_inst.get_info()
            external_id = fact_info["plugin_data"]["name"]
            if not DataWriter().facts.get_by_id(external_id):  # TODO: upsert
                DataWriter().facts.update_by_id(external_id, fact_info)


@App.task(name="engine:facts.flush")
def flush():
    DataWriter().facts.flush()


@App.task(name="engine:facts.info")
def info(fact_name):
    return DataWriter().facts.get_by_name(fact_name).to_json()
