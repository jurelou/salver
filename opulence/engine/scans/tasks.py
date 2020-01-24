import json
from datetime import datetime

from opulence import App
from opulence.common.utils import replace_dict_keys
from opulence.engine.database import DataWriter


@App.task(name="engine:scan.get")
def get(external_identifier):
    scan = json.loads(DataWriter().scans.get_by_id(external_identifier).get().to_json())
    scan["results"] = json.loads(
        DataWriter().results.get_by_scan_id(external_identifier).to_json()
    )
    scan["stats"]["start_date"] = datetime.strptime(
        scan["stats"]["start_date"], "%Y,%m,%d,%H,%M,%S,%f"
    ).isoformat()
    if "end_date" in scan["stats"]:
        scan["stats"]["end_date"] = datetime.strptime(
            scan["stats"]["end_date"], "%Y,%m,%d,%H,%M,%S,%f"
        ).isoformat()
    return scan


@App.task(name="engine:scan.list")
def _list():
    return DataWriter().scans.get().to_json()


@App.task(name="engine:scan.remove")
def remove(result_id):
    return DataWriter().scans.delete_by_id(result_id)


@App.task(name="engine:scan.flush")
def flush():
    DataWriter().scans.flush()


@App.task(name="engine:scan.start_scan")
def start_scan(eid, inputs, scan_type="Unknown"):
    scan_data = {"scan_type": scan_type}
    DataWriter().scans.create_or_update(eid, scan_data)

    for i in inputs:
        DataWriter().scans.add_input(eid, i.get_summary())


@App.task(name="engine:scan.stop_scan")
def stop_scan(eid):
    DataWriter().scans.stop(eid)
    DataWriter().algorithms.lpa()
    DataWriter().algorithms.page_rank()


@App.task(name="engine:scan.tree")
def tree(scan_id):
    result = DataWriter().scans.tree(scan_id)
    print("GOT RESULT", result)
    relations = []
    for link in result.graph().relationships:
        nodes = link.nodes
        relations.append(
            {"source": nodes[0].get("name"), "target": nodes[1].get("name")}
        )
    graph = result.data()[0]["value"]
    print(graph)

    def convert_function(v):
        if v == "_type":
            return "family"
        return "children" if v in ["entered", "collected"] else v

    res = {"root": replace_dict_keys(graph, convert_function), "links": relations}
    return res


@App.task(name="engine:scan.flat_result")
def flat_result(scan_id):
    response = []
    results = DataWriter().results.get_by_scan_id(scan_id)
    cache_collector_results = {}
    for result in results:
        if result.result_identifier not in cache_collector_results:
            cache_collector_results[result.result_identifier] = (
                DataWriter()
                .collector_results.get_by_id(result.result_identifier)
                .collector["plugin_data"]
            )

        node = DataWriter().results.get_node_by_value(result.summary)
        node_data = node.single().get("node", None)
        features = {}
        if node_data is not None:
            features = {
                "pagerank": node_data.get("pagerank"),
                "lpa": node_data.get("lpa")
            }

        collector_result = cache_collector_results[result.result_identifier]

        response.append(
            {
                "summary": result.summary,
                "features": features,
                "fields": result.fields,
                "fact_name": result.plugin_data["name"],
                "fact_description": result.plugin_data["description"],
                "fact_category": result.plugin_data["category"],
                "collector_name": collector_result["name"],
                "collector_description": collector_result["description"],
            }
        )
    return response


@App.task(name="engine:scan.new_result", ignore_result=True)
def new_result(result, eid):
    scan_data = result.get_info()
    DataWriter().results.add_many(eid, scan_data)
