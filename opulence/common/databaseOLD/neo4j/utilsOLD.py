# -*- coding: utf-8 -*-
from loguru import logger
from neo4j import GraphDatabase


def create_client(config):
    logger.info(f"Create neo4j client: {config}")
    return GraphDatabase.driver(
        config.endpoint, auth=(config.username, config.password),
    )


def create_constraints(client):
    logger.info("Create neo4j constraints")
    with client.session() as session:
        session.run(
            "CREATE CONSTRAINT case_unique_id IF NOT EXISTS ON (c:Case) ASSERT c.external_id IS UNIQUE",
        )
        session.run(
            "CREATE CONSTRAINT scan_unique_id IF NOT EXISTS ON (s:Scan) ASSERT s.external_id IS UNIQUE",
        )


def flush(client):
    logger.warning("Flush neo4j database")
    with client.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
