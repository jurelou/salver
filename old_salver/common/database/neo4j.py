# -*- coding: utf-8 -*-
import time
import uuid
from typing import Dict, List

from neo4j import GraphDatabase
from loguru import logger

from salver.common.models import BaseFact, CollectResult
from salver.common.database import models

from .base import BaseDB


class Neo4jDB(BaseDB):
    def __init__(self, config):
        logger.info(f'neo4j: Build with config {config}')
        self._client = GraphDatabase.driver(
            config.endpoint,
            auth=(config.username, config.password),
        )

    def flush(self):
        logger.warning(f'neo4j: Flush')
        with self._client.session() as session:
            session.run('MATCH (n) DETACH DELETE n')

    def bootstrap(self):
        logger.debug('neo4j: Bootstrap')
        with self._client.session() as session:
            session.run(
                'CREATE CONSTRAINT case_unique_id \
                IF NOT EXISTS ON (c:Case) ASSERT c.external_id IS UNIQUE',
            )
            session.run(
                'CREATE CONSTRAINT scan_unique_id \
                IF NOT EXISTS ON (s:Scan) ASSERT s.external_id IS UNIQUE',
            )

    def add_case(self, case: models.CaseInDB):
        """Create a new case."""
        logger.debug(f'neo4j: Add case {case.external_id}')
        with self._client.session() as session:
            session.run(
                'CREATE (case: Case {external_id: $external_id}) ',
                external_id=case.external_id.hex,
            )

    def add_scan(self, scan: models.ScanInDB):
        """Create a new scan and link it to an existing case."""
        logger.debug(f'neo4j: Add scan {scan.external_id}')

        with self._client.session() as session:
            session.run(
                'MATCH (case:Case) '
                'WHERE case.external_id = $cid '
                'MERGE (case)-[r:CONTAINS {timestamp: $ts}]->(scan:Scan {external_id: $sid})',
                ts=time.time(),
                cid=scan.case_id.hex,
                sid=scan.external_id.hex,
            )

    def add_facts(
        self,
        scan_id,
        facts: List[BaseFact],
        relationship: str = 'GIVES',
    ):
        """Add facts to a scan."""
        logger.debug(f'neo4j: Add {len(facts)} facts to scan {scan_id}')
        formated_facts = [
            {'external_id': fact.hash__, 'type': fact.schema()['title']}
            for fact in facts
        ]
        with self._client.session() as session:
            session.run(
                'MATCH (scan:Scan) '
                'WHERE scan.external_id = $scan_id '
                'UNWIND $facts as row '
                'MERGE (fact:Fact {external_id: row.external_id}) '
                'ON CREATE SET fact.type = row.type '
                'WITH fact, scan '
                'CALL apoc.create.relationship(scan, $reltype, {timestamp: $ts}, fact) '
                'YIELD rel '
                'RETURN rel',
                scan_id=scan_id.hex,
                facts=formated_facts,
                ts=time.time(),
                reltype=relationship,
            )

    def get_input_facts_for_scan(
        self,
        scan_id: uuid.UUID,
    ) -> Dict[str, List[uuid.UUID]]:
        """Get input facts for a given scan."""
        logger.debug(f'neo4j: Get input facts for scan {scan_id}')
        facts = {}
        with self._client.session() as session:
            result = session.run(
                'MATCH (scan:Scan {external_id: $eid})-[:INPUTS]->(fact:Fact) RETURN DISTINCT fact',
                eid=scan_id.hex,
            )
            for record in result:
                fact = record.get('fact')
                if not fact:  # pragma: no cover
                    continue

                fact_type = fact.get('type')
                fact_id = fact.get('external_id')
                if fact_type in facts:
                    facts[fact_type].append(fact_id)
                else:
                    facts[fact_type] = [fact_id]
        return facts

    def get_scans_for_case(self, case_id: uuid.UUID) -> List[uuid.UUID]:
        """Get scans for a given case."""
        logger.debug(f'neo4j: Get scans for case {case_id}')
        scans = []
        with self._client.session() as session:
            result = session.run(
                'MATCH (Case {external_id: $case_id})--(scan:Scan) RETURN scan',
                case_id=case_id.hex,
            )
            for record in result:
                scan = record.get('scan')
                if scan:
                    scans.append(scan.get('external_id'))
        return scans

    def add_scan_results(
        self,
        scan_id: uuid.UUID,
        result: CollectResult,
        relationship='OUTPUTS',
    ):
        """Add results to a given scan."""
        logger.debug(f'neo4j: Add results {result} to scan {scan_id}')
        with self._client.session() as session:
            session.run(
                'MATCH (scan:Scan) '
                'WHERE scan.external_id = $scan_id '
                'UNWIND $facts as row '
                'MERGE (fact:Fact {external_id: row}) '
                'WITH fact, scan '
                'CALL apoc.create.relationship(scan, $relationship, {timestamp: $timestamp}, fact) '
                'YIELD rel '
                'RETURN rel',
                scan_id=scan_id.hex,
                facts=result.facts,
                timestamp=time.time(),
                relationship=relationship,
            )