# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

import pymongo
from loguru import logger
from pymongo.errors import DuplicateKeyError

from salver.controller import models
from salver.common.models import BaseFact, ScanResult
from salver.controller.services.database import exceptions

from .base import BaseDB


class MongoDB(BaseDB):
    def __init__(self, config):
        print(f"Build mongodb with {config}")
        self._client = pymongo.MongoClient(config.endpoint)
        self._db_name = config.database
        self._db = self._client[config.database]
        print(self._client.server_info()["version"])

    def flush(self):
        logger.warning("Flush neo4j database")
        self._client.drop_database(self._db_name)

    def bootstrap(self):
        logger.info("Create neo4j constraints")
        self._db.cases.create_index("name", unique=True)

    def add_case(self, case: models.CaseInDB) -> None:
        try:
            self._db.cases.insert_one(case.dict())
        except DuplicateKeyError as err:
            raise exceptions.CaseAlreadyExists(case.external_id) from err

    def add_scan(self, scan: models.ScanInDB):
        self._db.scans.insert_one(scan.dict())

    def get_scan(self, scan_id) -> models.ScanInDB:
        scan = self._db.scans.find_one({"external_id": scan_id})
        if not scan:
            raise exceptions.ScanNotFound(scan_id)
        return models.ScanInDB(**scan)

    def case_exists(self, case_id: UUID) -> bool:
        return self._db.cases.count_documents({"external_id": case_id}) > 0

    def get_case(self, case_id: UUID) -> models.CaseInDB:
        case = self._db.cases.find_one({"external_id": case_id})  # find().limit(1)
        if not case:
            raise exceptions.CaseNotFound(case_id)
        return models.CaseInDB(**case)

    def update_scan_state(self, scan_id, state: models.ScanState):
        self._db.scans.update_one(
            {"external_id": scan_id},
            {"$set": {"state": state.value}},
        )

    def add_scan_results(self, scan_id: UUID, result: ScanResult):
        self._db.scans.update_one(
            {"external_id": scan_id},
            {"$set": result.dict(exclude={"facts"})},
        )
