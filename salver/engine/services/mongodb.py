# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

import pymongo
from loguru import logger
from pymongo.errors import DuplicateKeyError
from salver.config import engine_config
from salver.common import models
import time

MONGO_CLIENT =  pymongo.MongoClient(engine_config.mongo.url)

def bootstrap():
    logger.info('Bootstrap mongodb')
    MONGO_CLIENT.agents.create_index('name', unique=True)

# class MongoDB(BaseDB):
#     def __init__(self, config):
#         self._client = pymongo.MongoClient(config.endpoint)
#         self._db_name = config.database
#         self._db = self._client[config.database]
#         logger.info(
#             f'mongodb: Build version {self._client.server_info()["version"]} with {config}',
#         )

#     def flush(self):
#         logger.info(f'mongodb: Flush')
#         self._client.drop_database(self._db_name)

#     def bootstrap(self):
#         logger.debug(f'mongodb: Boostrap')
#         self._db.cases.create_index('name', unique=True)

#     def add_case(self, case: db_models.CaseInDB) -> None:
#         """Add a new case."""
#         logger.debug(f'mongodb: Add case {case.external_id}')
#         try:
#             self._db.cases.insert_one(case.dict())
#         except DuplicateKeyError as err:
#             raise exceptions.CaseAlreadyExists(case.name) from err

#     def add_scan(self, scan: db_models.ScanInDB):
#         """Add a new scan."""
#         logger.debug(f'mongodb: Add scan {scan.external_id}')
#         self._db.scans.insert_one(scan.dict())

#     def get_scan(self, scan_id) -> db_models.ScanInDB:
#         """Get a scan by it's ID."""
#         logger.debug(f'mongodb: Get scan {scan_id}')
#         scan = self._db.scans.find_one({'external_id': scan_id})
#         if not scan:
#             raise exceptions.ScanNotFound(scan_id)
#         return db_models.ScanInDB(**scan)

#     def case_exists(self, case_id: UUID) -> bool:
#         """Check if a given case exists."""
#         logger.debug(f'mongodb: check case {case_id} exists')
#         return self._db.cases.count_documents({'external_id': case_id}) > 0

#     def get_case(self, case_id: UUID) -> db_models.CaseInDB:
#         """Get a case by it's ID."""
#         logger.debug(f'mongodb: Get case {case_id}')
#         case = self._db.cases.find_one({'external_id': case_id})  # find().limit(1)
#         if not case:
#             raise exceptions.CaseNotFound(case_id)
#         return db_models.CaseInDB(**case)

#     def update_scan_state(self, scan_id, state: ScanState):
#         """Update a scan state."""
#         logger.debug(f'mongodb: Set scan {scan_id} state to {state}')
#         self._db.scans.update_one(
#             {'external_id': scan_id},
#             {'$set': {'state': state.value}},
#         )

#     def add_scan_results(self, scan_id: UUID, result: CollectResult):
#         self._db.scans.update_one(
#             {"external_id": scan_id},
#             {"$set": result.dict(exclude={"facts"})},
#         )

#     def list_scans(self) -> List[UUID]:
#         """Get all scans IDs."""
#         logger.debug(f'mongodb: List scans')
#         ids = self._db.scans.find({}, {'external_id': True, '_id': False})
#         return [i['external_id'] for i in ids]

#     def list_cases(self) -> List[UUID]:
#         """Get all cases IDs."""
#         logger.debug(f'mongodb: List cases')
#         ids = self._db.cases.find({}, {'external_id': True, '_id': False})
#         return [i['external_id'] for i in ids]
