import pymongo

from loguru import logger
from opulence.engine.database.base import BaseDB
from opulence.common import models

class   MongoDB(BaseDB):
    def __init__(self, config):
        print(f"Build mongodb with {config}")
        self._client = pymongo.MongoClient(config.endpoint)
        self._db = self._client.opulence
        print(self._client.server_info()["version"])

    def flush(self):
        logger.warning("Flush neo4j database")
        self._client.drop_database('opulence')


    def bootstrap(self):
        logger.info("Create neo4j constraints")
        self._db.cases.create_index(
            "name", unique=True
        )

    def add_case(self, case: models.Case):
        res = self._db.cases.insert_one(case.dict())
        #TODO:catch pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: opulence.cases index: name_1 dup key: { name: "toto" }, full error: {'index': 0, 'code': 11000, 'keyPattern': {'name': 1}, 'keyValue': {'name': 'toto'}, 'errmsg': 'E11000 duplicate key error collection: opulence.cases index: name_1 dup key: { name: "toto" }'}
        return res.inserted_id

    def add_scan(self, scan: models.Scan):
        print("GO", scan)
