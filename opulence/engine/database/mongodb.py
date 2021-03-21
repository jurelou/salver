# -*- coding: utf-8 -*-
import pymongo
from typing import List
from loguru import logger
from opulence.engine.database.base import BaseDB
from opulence.common import models
from uuid import UUID
from opulence.engine.database import exceptions


class MongoDB(BaseDB):
    def __init__(self, config):
        print(f"Build mongodb with {config}")
        self._client = pymongo.MongoClient(config.endpoint)
        self._db = self._client.opulence
        print(self._client.server_info()["version"])

    def flush(self):
        logger.warning("Flush neo4j database")
        self._client.drop_database("opulence")

    def bootstrap(self):
        logger.info("Create neo4j constraints")
        self._db.cases.create_index("name", unique=True)

    def add_case(self, case: models.Case):
        res = self._db.cases.insert_one(case.dict())
        # TODO:catch pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: opulence.cases index: name_1 dup key: { name: "toto" }, full error: {'index': 0, 'code': 11000, 'keyPattern': {'name': 1}, 'keyValue': {'name': 'toto'}, 'errmsg': 'E11000 duplicate key error collection: opulence.cases index: name_1 dup key: { name: "toto" }'}
        return res.inserted_id

    def add_scan(self, scan: models.Scan):
        # scan_dict = scan.dict(exclude={"facts"})
        # scan_dict["state"] = scan_dict["state"].value
        res = self._db.scans.insert_one(scan.dict(exclude={"facts"}))
        return res.inserted_id

    def get_scan(self, scan_id) -> models.Scan:
        scan = self._db.scans.find_one({"external_id": scan_id})
        if not scan:
            raise exceptions.ScanNotFound(scan_id)
        return models.Scan(**scan)

    def case_exists(self, case_id: UUID) -> bool:
        return self._db.cases.count_documents({"external_id": case_id}) > 0

    def get_case(self, case_id) -> models.Case:
        case = self._db.cases.find_one({"external_id": case_id})  # find().limit(1)
        if not case:
            raise exceptions.CaseNotFound(case_id)
        return models.Case(**case)

    def update_scan_state(self, scan_id, state: models.ScanState):
        self._db.scans.update_one(
            {"external_id": scan_id}, {"$set": {"state": state.value}}
        )

    def add_scan_results(self, scan_id: UUID, result: models.ScanResult):
        self._db.scans.update_one({"external_id": scan_id}, {"$set": result.dict()})
