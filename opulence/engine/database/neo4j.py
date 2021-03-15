from neo4j import GraphDatabase
from loguru import logger
from opulence.engine.database.base import BaseDB

class   Neo4jDB(BaseDB):
    def __init__(self, config):
        print(f"Build neo4j with {config}")
        self._client = GraphDatabase.driver(
            config.endpoint, auth=(config.username, config.password),
        )

    def flush(self):
        logger.warning("Flush neo4j database")
        with self._client.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    
    def bootstrap(self):
        logger.info("Create neo4j constraints")
        with self._client.session() as session:
            session.run(
                "CREATE CONSTRAINT case_unique_id IF NOT EXISTS ON (c:Case) ASSERT c.external_id IS UNIQUE",
            )
            session.run(
                "CREATE CONSTRAINT scan_unique_id IF NOT EXISTS ON (s:Scan) ASSERT s.external_id IS UNIQUE",
            )
