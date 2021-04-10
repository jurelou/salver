# -*- coding: utf-8 -*-
import uuid
from typing import List

from salver.config import controller_config
from salver.controller import models
from salver.common.models import BaseFact, ScanResult

from . import exceptions
from .neo4j import Neo4jDB
from .mongodb import MongoDB
from .elasticsearch import ElasticsearchDB


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

    def add_case(self, case: models.CaseInRequest) -> uuid.UUID:
        """Adds a Case to the databases.

        Cases are stored in mongodb and neo4j.
        Args:
            case (CaseInRequest): a Case instance to store.

        Returns:
            uuid.UUID: The case identifier
        """
        case_db = models.CaseInDB(**case.dict())

        self.neo4j.add_case(case_db)
        self.mongodb.add_case(case_db)

        return case_db.external_id

    def add_scan(self, scan: models.ScanInRequest) -> uuid.UUID:
        """Adds a Scan to the databases.

        Scans are stored in mongodb and neo4j.
        Args:
            scan (Scan): a Scan instance to store.

        Returns:
            uuid.UUID: the scan identifier
        Raises:
            AttributeError: The ``Raises`` section is a list of all exceptions
                that are relevant to the interface.
        """
        if not self.mongodb.case_exists(scan.case_id):
            raise exceptions.CaseNotFound(scan.case_id)

        scan_db = models.ScanInDB(**scan.dict(exclude={"facts"}))
        scan_db.state = models.ScanState.CREATED

        self.elasticsearch.add_facts(scan.facts)
        self.neo4j.add_scan(scan_db)
        self.neo4j.add_facts(scan_db.external_id, scan.facts, relationship="INPUTS")

        self.mongodb.add_scan(scan_db)
        return scan_db.external_id

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
        # facts_ids = self.neo4j.get_scan_input_facts(scan_id)
        # facts = list(self.elasticsearch.get_facts(facts_ids))

        # scan.facts = facts
        return scan

    def get_case(self, case_id: uuid.UUID) -> models.CaseInDB:
        """Retrieve a case by it's ID.

        Args:
            case_id (UUID): the case ID's.

        Returns:
            Case: A Case Instance
        Raises:
            CaseNotFound: If the case does not exists.
        """
        return self.mongodb.get_case(case_id)

    def get_scans_for_case(self, case_id: uuid.UUID) -> List[uuid.UUID]:
        return self.neo4j.get_scans_for_case(case_id)

    def get_input_facts_for_scan(self, scan_id: uuid.UUID) -> List[BaseFact]:
        facts_id = self.neo4j.get_input_facts_for_scan(scan_id)
        return self.elasticsearch.get_facts(facts_id)

    def add_scan_results(self, scan_id: uuid.UUID, scan_result: ScanResult):
        print(f"Add result to scan {scan_id}, {scan_result}")
        self.mongodb.add_scan_results(scan_id, scan_result)
        self.neo4j.add_scan_results(scan_id, scan_result)
