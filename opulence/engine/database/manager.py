from opulence.config import engine_config
from opulence.engine.database.neo4j import Neo4jDB
from opulence.engine.database.elasticsearch import ElasticsearchDB
from opulence.engine.database.mongodb import MongoDB
from opulence.common import models
import uuid

class   DatabaseManager:
    def __init__(self):
        self._neo4j = Neo4jDB(config=engine_config.neo4j)
        self._elasticsearch = ElasticsearchDB(config=engine_config.elasticsearch)
        self._mongodb = MongoDB(config=engine_config.mongodb)

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
    
    def add_case(self, case: models.Case):
        self.neo4j.add_case(case)
        return self.mongodb.add_case(case)

    def add_scan(self, scan: models.Scan):
        self.elasticsearch.add_facts(scan.facts)
        self.neo4j.add_scan(scan)
        return self.mongodb.add_scan(scan)
    
    def get_scan(self, scan_id: uuid.UUID) -> models.Scan:
        facts_ids = self.neo4j.get_scan_input_facts(scan_id)
        facts = list(self.elasticsearch.get_facts(facts_ids))

        scan = self.mongodb.get_scan(scan_id)
        scan.facts = facts
        return scan
    
    def get_case(self, case_id: uuid.UUID) -> models.Case:
        case = self.mongodb.get_case(case_id)
        return case

