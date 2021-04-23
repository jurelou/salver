# -*- coding: utf-8 -*-
import uuid
from typing import List

from salver.common import models as common_models
from salver.common.models import BaseFact, ScanResult
from salver.common.database import models as db_models

from . import exceptions
from .base import BaseDB
from .neo4j import Neo4jDB
from .mongodb import MongoDB
from .elasticsearch import ElasticsearchDB


class DatabaseManager:
    def __init__(self, neo4j_config, elasticsearch_config, mongodb_config):
        self._neo4j = Neo4jDB(config=neo4j_config)
        self._elasticsearch = ElasticsearchDB(config=elasticsearch_config)
        self._mongodb = MongoDB(config=mongodb_config)

    def flush(self):
        [db.flush() for db in self.databases]

    def bootstrap(self):
        [db.bootstrap() for db in self.databases]

    @property
    def neo4j(self) -> Neo4jDB:
        return self._neo4j

    @property
    def mongodb(self) -> MongoDB:
        return self._mongodb

    @property
    def elasticsearch(self) -> ElasticsearchDB:
        return self._elasticsearch

    @property
    def databases(self) -> List[BaseDB]:
        return [self.mongodb, self.neo4j, self.elasticsearch]

    def update_scan_state(self, scan_id, state: common_models.ScanState):
        self.mongodb.update_scan_state(scan_id, state)

    def add_case(self, case) -> uuid.UUID:
        """Adds a Case to the databases.

        Cases are stored in mongodb and neo4j.
        Args:
            case (Case): a Case instance to store.

        Returns:
            uuid.UUID: The case identifier
        """
        case_db = db_models.CaseInDB(**case.dict())

        self.neo4j.add_case(case_db)
        self.mongodb.add_case(case_db)

        return case_db.external_id

    def add_scan(self, scan) -> uuid.UUID:
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

        scan_db = db_models.ScanInDB(**scan.dict())
        scan_db.state = common_models.ScanState.CREATED
        self.neo4j.add_scan(scan_db)
        self.mongodb.add_scan(scan_db)
        return scan_db.external_id

    def add_scan_input_facts(self, scan_id: uuid.UUID, facts: List[BaseFact]):
        self.elasticsearch.add_facts(facts)
        self.neo4j.add_facts(scan_id, facts, relationship="INPUTS")

    def get_scan(self, scan_id: uuid.UUID) -> db_models.ScanInDB:
        """Retrieve a scan by it's ID.

        Args:
            scan_id (UUID): the scan ID's.

        Returns:
            Scan: A Scan Instance
        Raises:
            ScanNotFound: If the scan does not exists.
        """
        return self.mongodb.get_scan(scan_id)

    def list_scans(self) -> List[uuid.UUID]:
        return self.mongodb.list_scans()

    def list_cases(self) -> List[uuid.UUID]:
        return self.mongodb.list_cases()

    def get_case(self, case_id: uuid.UUID) -> db_models.CaseInDB:
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
        res = self.elasticsearch.get_facts(facts_id)
        return res

    def add_scan_results(self, scan_id: uuid.UUID, scan_result: ScanResult):
        # self.mongodb.add_scan_results(scan_id, scan_result)
        self.neo4j.add_scan_results(scan_id, scan_result)
