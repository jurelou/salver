# -*- coding: utf-8 -*-
import multiprocessing

from celery.utils.log import get_task_logger
from dynaconf import settings

from opulence import App
from opulence.common.job import Result
from opulence.common.job import StatusCode
from opulence.common.plugins import PluginManager

logger = get_task_logger(__name__)


manager = multiprocessing.Manager()
available_collectors = manager.dict()


@App.task(name="collectors:reload_collectors", ignore_result=True)
def reload_collectors(flush=False):
    global available_collectors
    logger.info("Reload collectors")
    if flush:
        available_collectors.clear()
    for path in settings.COLLECTORS_MODULES:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name not in available_collectors:
                available_collectors[plugin.plugin_name] = plugin


@App.task(name="collectors:list_collectors")
def list_collectors():
    global available_collectors
    logger.info("List collectors")
    return [c.get_info() for _, c in available_collectors.items()]


@App.task(name="collectors:execute_collector_by_name")
def execute_collector_by_name(collector_name, fact_or_composite):
    global available_collectors
    logger.info(
        "Execute collector {} with {}".format(collector_name, type(fact_or_composite)),
    )
    result = Result(input=fact_or_composite, status=StatusCode.empty)
    if collector_name in available_collectors:
        return available_collectors[collector_name].run(result)
    result.status = (
        StatusCode.error,
        f"Could not find collector {collector_name}",
    )
    return result


# Reload collectors at startup
reload_collectors(flush=True)
[
    print(
        "{} ({})".format(
            i["plugin_data"]["name"],
            i["plugin_data"]["error"] if i["plugin_data"]["error"] else "OK",
        ),
    )
    for i in list_collectors()
]
