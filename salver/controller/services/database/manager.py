# -*- coding: utf-8 -*-
from salver.config import controller_config
from .neo4j import Neo4jDB
from .elasticsearch import ElasticsearchDB
from .mongodb import MongoDB
from salver.controller import models
from salver.common.models import ScanResult
from . import exceptions
import uuid


class DatabaseManager:
    def __init__(self):
        self._neo4j = Neo4jDB(config=controller_config.neo4j)
        self._elasticsearch = ElasticsearchDB(config=controller_config.elasticsearch)
        self._mongodb = MongoDB(config=controller_config.mongodb)

    def flush(self):
        for db in self.databases:
            db.flush()

    def bootstrap(self):
        for db in self.databases:
            db.bootstrap()

    @property
    def neo4j(self):
        return self._neo4j

    @property
    def mongodb(self):
        return self._mongodb

    @property
    def elasticsearch(self):
        return self._elasticsearch

    @property
    def databases(self):
        return [self.mongodb, self.neo4j, self.elasticsearch]

    def update_scan_state(self, scan_id, state: models.ScanState):
        self.mongodb.update_scan_state(scan_id, state)

    def add_case(self, case: models.Case):
        """Adds a Case to the databases.

        Cases are stored in mongodb and neo4j.
        Args:
            case (Case): a Case instance to store.

        Returns:
            bool: The return value. True for success, False otherwise.
        """
        self.neo4j.add_case(case)
        return self.mongodb.add_case(case)

    def add_scan(self, scan: models.ScanInDB):
        """Adds a Scan to the databases.

        Scans are stored in mongodb and neo4j.
        Args:
            scan (Scan): a Scan instance to store.

        Returns:
            bool: The return value. True for success, False otherwise.
        Raises:
            AttributeError: The ``Raises`` section is a list of all exceptions
                that are relevant to the interface.
            ValueError: If `param2` is equal to `param1`.
        """
        if not self.mongodb.case_exists(scan.case_id):
            raise exceptions.CaseNotFound(scan.case_id)

        scan.state = models.ScanState.CREATED
        self.elasticsearch.add_facts(scan.facts)
        self.neo4j.add_scan(scan)
        return self.mongodb.add_scan(scan)

    def get_scan(self, scan_id: uuid.UUID) -> models.ScanInDB:
        """Retrieve a scan by it's ID.

        Args:
            scan_id (UUID): the scan ID's.

        Returns:
            Scan: A Scan Instance
        Raises:
            ScanNotFound: If the scan does not exists.
        """
        scan = self.mongodb.get_scan(scan_id)
        facts_ids = self.neo4j.get_scan_input_facts(scan_id)
        facts = list(self.elasticsearch.get_facts(facts_ids))

        scan.facts = facts
        return scan

    def get_case(self, case_id: uuid.UUID) -> models.Case:
        """Retrieve a case by it's ID.

        Args:
            case_id (UUID): the case ID's.

        Returns:
            Case: A Case Instance
        Raises:
            CaseNotFound: If the case does not exists.
        """
        case = self.mongodb.get_case(case_id)
        return case

    def add_scan_results(self, scan_id: uuid.UUID, scan_result: ScanResult):
        # logger.info(f"Add result to scan {scan_id}")
        self.mongodb.add_scan_results(scan_id, scan_result)
        self.neo4j.add_scan_results(scan_id, scan_result)
