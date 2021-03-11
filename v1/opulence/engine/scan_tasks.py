from celery import group

from opulence import App
import opulence.collectors.signatures as remote_ctrl
from opulence.common.utils import generate_uuid
from opulence.common.utils import is_list
from opulence.engine.database import DataWriter
from opulence.facts import services as facts_services

from .scans import signatures as scan_ctrl


@App.task(name="engine:scan.quick")
def quick_scan(collector_name, facts):
    external_id = generate_uuid().hex
    f = facts_services.fact_from_json(facts)
    c = (
        scan_ctrl.start(external_id, [f])
        | remote_ctrl.launch(collector_name, f)
        | scan_ctrl.add_result(external_id)
        | scan_ctrl.stop(external_id)
    )
    c.apply_async()
    return external_id


@App.task(name="engine:scan.full")
def full_scan(facts):
    external_id = generate_uuid().hex
    if not is_list(facts):
        facts = [facts]
    fact_cls = facts_services.facts_from_json(facts)

    tasks = []
    for f in fact_cls:
        available_collectors = DataWriter().collectors.find_by_allowed_input(
            f.plugin_name,
        )
        for ac in available_collectors:
            tasks.append(remote_ctrl.launch(ac, f) | scan_ctrl.add_result(external_id))

    tasks_group = group(tasks)
    workflow = (
        scan_ctrl.start(external_id, fact_cls, "Full scan")
        | tasks_group
        | scan_ctrl.stop(external_id)
    )

    workflow.apply_async()
    return external_id
