# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

import pymongo
from loguru import logger
from pymongo.errors import DuplicateKeyError

from salver.common.models import BaseFact, ScanState, ScanResult
from salver.common.database import models as db_models
from salver.common.database import exceptions

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

    def add_case(self, case: db_models.CaseInDB) -> None:
        try:
            self._db.cases.insert_one(case.dict())
        except DuplicateKeyError as err:
            raise exceptions.CaseAlreadyExists(case.external_id) from err

    def add_scan(self, scan: db_models.ScanInDB):
        self._db.scans.insert_one(scan.dict())

    def get_scan(self, scan_id) -> db_models.ScanInDB:
        scan = self._db.scans.find_one({"external_id": scan_id})
        if not scan:
            raise exceptions.ScanNotFound(scan_id)
        return db_models.ScanInDB(**scan)

    def case_exists(self, case_id: UUID) -> bool:
        return self._db.cases.count_documents({"external_id": case_id}) > 0

    def get_case(self, case_id: UUID) -> db_models.CaseInDB:
        case = self._db.cases.find_one({"external_id": case_id})  # find().limit(1)
        if not case:
            raise exceptions.CaseNotFound(case_id)
        return db_models.CaseInDB(**case)

    def update_scan_state(self, scan_id, state: ScanState):
        self._db.scans.update_one(
            {"external_id": scan_id},
            {"$set": {"state": state.value}},
        )

    # def add_scan_results(self, scan_id: UUID, result: ScanResult):
    #     self._db.scans.update_one(
    #         {"external_id": scan_id},
    #         {"$set": result.dict(exclude={"facts"})},
    #     )

    def list_scans(self) -> List[UUID]:
        ids = self._db.scans.find({}, {"external_id": True, "_id": False})
        return [i["external_id"] for i in ids]

    def list_cases(self) -> List[UUID]:
        ids = self._db.cases.find({}, {"external_id": True, "_id": False})
        return [i["external_id"] for i in ids]
