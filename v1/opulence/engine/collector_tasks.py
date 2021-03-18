# -*- coding: utf-8 -*-
from opulence import App
import opulence.collectors.signatures as collectors_s
from opulence.engine.database import DataWriter


@App.task(name="engine:collectors.get")
def get():
    return DataWriter().collectors.get().to_json()


@App.task(name="engine:collectors.load")
def load():
    store_result = App.signature("engine:__store_collectors")

    chain = collectors_s.load() | collectors_s.list() | store_result
    chain.apply_async()


@App.task(name="engine:collectors.flush")
def flush():
    DataWriter().collectors.flush()


@App.task(name="engine:collectors.info")
def info(external_identifier):
    return DataWriter().collectors.get_by_id(external_identifier).to_json()


@App.task(name="engine:collectors.launch")
def launch(collector_name, fact):
    return collectors_s.launch(collector_name, fact).apply_async()


@App.task(name="engine:__store_collectors")
def __store_collectors(collectors):
    for collector_data in collectors:
        collector_id = collector_data["plugin_data"]["name"]
        if not DataWriter().collectors.get_by_id(collector_id):
            DataWriter().collectors.update_by_id(collector_id, collector_data)
