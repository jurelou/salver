# -*- coding: utf-8 -*-
from typing import List
from uuid import uuid4

from loguru import logger

from opulence.common.database.es import facts as es_facts
from opulence.common.database.neo4j import facts as neo4j_facts
from opulence.common.models.fact import BaseFact
from opulence.engine.app import es_client
from opulence.engine.app import neo4j_client


def add_many(facts: List[BaseFact]):
    logger.info(f"Add {len(facts)} facts")
    es_facts.bulk_upsert(es_client, facts)
    neo4j_facts.add_many(neo4j_client, facts)


def get_many(facts_ids: List[uuid4]):
    logger.info(f"Get facts {facts_ids}")
    facts = es_facts.get_many(es_client, facts_ids)
    return facts
