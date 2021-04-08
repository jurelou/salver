# -*- coding: utf-8 -*-
from neo4j import GraphDatabase
from loguru import logger
from .base import BaseDB
from salver.common.models import BaseFact, ScanResult
from salver.controller import models
from typing import List
import time
import uuid


class Neo4jDB(BaseDB):
    def __init__(self, config):
        print(f"Build neo4j with {config}")
        self._client = GraphDatabase.driver(
            config.endpoint,
            auth=(config.username, config.password),
        )

    def flush(self):
        logger.warning("Flush neo4j database")
        with self._client.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def bootstrap(self):
        logger.info("Create neo4j constraints")
        with self._client.session() as session:
            session.run(
                "CREATE CONSTRAINT case_unique_id IF NOT EXISTS ON (c:Case) ASSERT c.external_id IS UNIQUE",
            )
            session.run(
                "CREATE CONSTRAINT scan_unique_id IF NOT EXISTS ON (s:Scan) ASSERT s.external_id IS UNIQUE",
            )

    def add_case(self, case: models.CaseInDB):
        with self._client.session() as session:
            session.run(
                "CREATE (case: Case {external_id: $external_id}) ",
                external_id=case.external_id.hex,
            )

    def add_facts(
        self,
        scan_id,
        facts: List[BaseFact],
        relationship: str = "GIVES",
    ):
        formated_facts = [
            {"external_id": fact.hash__, "type": fact.schema()["title"]}
            for fact in facts
        ]
        with self._client.session() as session:
            session.run(
                "MATCH (scan:Scan) "
                "WHERE scan.external_id = $scan_id "
                "UNWIND $facts as row "
                "MERGE (fact:Fact {external_id: row.external_id}) "
                "ON CREATE SET fact.type = row.type "
                "WITH fact, scan "
                "CALL apoc.create.relationship(scan, $relationship, {timestamp: $timestamp}, fact) "
                "YIELD rel "
                "RETURN rel",
                scan_id=scan_id.hex,
                facts=formated_facts,
                timestamp=time.time(),
                relationship=relationship,
            )

    def add_scan(self, scan: models.ScanInDB):
        with self._client.session() as session:
            session.run(
                "MATCH (case:Case) "
                "WHERE case.external_id = $case_id "
                "MERGE (case)-[r:CONTAINS {timestamp: $timestamp}]->(scan:Scan {external_id: $scan_id})",
                timestamp=time.time(),
                case_id=scan.case_id.hex,
                scan_id=scan.external_id.hex,
            )

    def get_scan_input_facts(self, scan_id: uuid.UUID):  # -> Dict[str, List[uuid.UUID]]
        facts = {}
        with self._client.session() as session:
            result = session.run(
                "MATCH (scan: Scan {external_id: $external_id})-[r: INPUTS]->(fact:Fact) "
                "RETURN DISTINCT fact",
                external_id=scan_id.hex,
            )
            for i, record in enumerate(result):
                for node in record:
                    fact_type = node.get("type")
                    fact_id = node.get("external_id")
                    if fact_type in facts:
                        facts[fact_type].append(fact_id)
                    else:
                        facts[fact_type] = [fact_id]
        return facts


    def get_scans_for_case(self, case_id:uuid.UUID) -> List[uuid.UUID]:
        scans = []
        with self._client.session() as session:
            result = session.run(
                "MATCH (Case {external_id: $case_id})--(scan:Scan) RETURN scan",
                case_id=case_id.hex,
            )
            for record in result:
                scan = record.get("scan")
                if scan:
                    scans.append(scan.get("external_id"))
        return scans

    def add_scan_results(
        self,
        scan_id: uuid.UUID,
        result: ScanResult,
        relationship="OUTPUTS",
    ):
        with self._client.session() as session:
            session.run(
                "MATCH (scan:Scan) "
                "WHERE scan.external_id = $scan_id "
                "UNWIND $facts as row "
                "MERGE (fact:Fact {external_id: row}) "
                "WITH fact, scan "
                "CALL apoc.create.relationship(scan, $relationship, {timestamp: $timestamp}, fact) "
                "YIELD rel "
                "RETURN rel",
                scan_id=scan_id.hex,
                facts=result.facts,
                timestamp=time.time(),
                relationship=relationship,
            )
