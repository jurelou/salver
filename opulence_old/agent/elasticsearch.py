# -*- coding: utf-8 -*-
from elasticsearch.helpers import bulk
from opulence.facts import all_facts
from loguru import logger
from elasticsearch import Elasticsearch
from opulence.config import agent_config

# Create ES instance
es_client = Elasticsearch(hosts=[agent_config.elasticsearch.endpoint])


__facts_index_mapping = [(fact, f"facts_{fact.lower()}") for fact in all_facts.keys()]
fact_to_index = lambda fact: [i for f, i in __facts_index_mapping if f == fact][0]


def bulk_upsert(facts):
    def gen_actions(facts):
        logger.info(f"Upsert fact: {len(facts)}")
        for fact in facts:
            yield {
                "_op_type": "update",
                "_index": fact_to_index(fact.schema()["title"]),
                "_id": fact.hash__,
                "upsert": fact.dict(exclude={"hash__"}),
                "doc": fact.dict(exclude={"first_seen", "hash__"}),
            }

    bulk(client=es_client, actions=gen_actions(facts))
