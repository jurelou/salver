# -*- coding: utf-8 -*-
from dynaconf import settings
from neo4j import GraphDatabase


class Algorithms:
    def __init__(self, client):
        self.client = client

    def page_rank(self):
        with self.client.session() as session:
            session.run(
                "CALL algo.pageRank('Result', 'COLLECTED', {iterations:20, dampingFactor:0.85, write: true, writeProperty: 'pagerank'}) "
                "YIELD nodes, iterations, loadMillis, computeMillis, writeMillis, dampingFactor, write, writeProperty ",
            )

    def lpa(self):
        with self.client.session() as session:
            session.run(
                "CALL algo.labelPropagation('Result', 'COLLECTED', {iterations: 10, writeProperty: 'lpa', write: true, direction: 'INCOMING'}) "
                "YIELD nodes, iterations, loadMillis, computeMillis, writeMillis, write, writeProperty; ",
            )


class Results:
    def __init__(self, client):
        self.client = client

    def get_node_by_value(self, value):
        with self.client.session() as session:
            return session.run(
                "MATCH (node: Result) " "WHERE node.name=$value " "RETURN node",
                value=value,
            )

    def add_many(self, results):
        with self.client.session() as session:
            for output in results["output"]:
                for input in results["input"]:
                    fields = output["fields"]
                    for k, v in fields.items():
                        fields[k] = v["value"]
                    session.run(
                        "MATCH (s: Result) "
                        "WHERE s.name=$input_summary "
                        "MERGE (r:Result {name: $output_summary}) "
                        "MERGE (s)-[:COLLECTED]->(r) "
                        "SET r += $values",
                        output_summary=output["summary"],
                        input_summary=input["summary"],
                        values=fields,
                    )


class Scans:
    def __init__(self, client):
        self.client = client

    def delete_by_id(self, identifier):
        with self.client.session() as session:
            session.run(
                "MATCH (r:Result {sid: $sid}) "
                "MATCH (c:Collected {sid: $sid}) "
                "MATCH (s:Scan {name: $sid})"
                "DETACH DELETE r,c,s",
                sid=identifier,
            )

    def _remove_self_relationships(self):
        with self.client.session() as session:
            session.run("MATCH (r:Result)-[rel:COLLECTED]->(r) " "DELETE rel")

    def tree(self, scan_id):
        with self.client.session() as session:
            self._remove_self_relationships()
            return session.run(
                "MATCH path = (s:Scan {name: $sid})-[:ENTERED|COLLECTED*]->(r:Result) "
                "WITH COLLECT(path)[..$max_results] AS paths "
                "CALL apoc.convert.toTree(paths) yield value "
                "RETURN value, paths ",
                sid=scan_id,
                max_results=settings.DB_QUERY_LIMIT.neo_max_connections,
            )

    def create_or_update(self, scan_name, data):
        with self.client.session() as session:
            session.run(
                "MERGE (s:Scan {name: $scan_name}) " "SET s += $data",
                scan_name=scan_name,
                data=data,
            )

    def add_input(self, scan_id, input_id):
        with self.client.session() as session:
            session.run(
                "MATCH (s: Scan) "
                "WHERE s.name=$sid "
                "MERGE (r:Result {name: $result_summary}) "
                "MERGE (s)-[:COLLECTED]-(r) ",
                result_summary=input_id,
                sid=scan_id,
            )

    def flush(self):
        with self.client.session() as session:
            session.run("MATCH (n) DETACH DELETE n")


class NeoDriver:
    def __init__(self):
        config = settings.GRAPH_DATABASE
        client = GraphDatabase.driver(
            config.url,
            auth=(config.user, config.password),
            encrypted=False,
            connection_timeout=10000,
            connection_acquisition_timeout=10000,
        )
        self.scans = Scans(client)
        self.results = Results(client)
        self.algorithms = Algorithms(client)
