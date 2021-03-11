# TODO:

- exceptions dans common/exceptions + print stacktrace dans l'exception de base
- exceptions

Traceback (most recent call last):
  File "/home/louis/binome/opulence/engine/tasks.py", line 61, in launch_scan
    scan = scan_ctrl.get(scan_id)
  File "/home/louis/binome/opulence/engine/controllers/scan.py", line 29, in get
    scan, facts = neo4j_scans.get_user_input_facts(neo4j_client, scan_id)
  File "/home/louis/binome/opulence/common/database/neo4j/scans.py", line 19, in get_user_input_facts
    scan = data[0]["scan"]
IndexError: list index out of range


# noms:

*inoma


binome

thoth

ocaro

ocai


relations = [{'from': 'man', 'to': 'woman', 'properties': {'cost': 0}},
{'from': 'woman', 'to': 'baby', 'properties': {'cost': 0}]


 query = """
    UNWIND {{relations}} as row
    MATCH (from:SINGLE_NODE {{name:row.from}})
    MATCH (to:SINGLE_NODE {{name:row.to}})
    MERGE (from)-[rel:IS_CONNECTED]->(to)
    ON CREATE SET rel += row.properties
    """.format(relations=relations)

    session.run(query, relations=relations)


session.run(query, relations=relations)
