# -*- coding: utf-8 -*-
from uuid import UUID
from typing import List

from loguru import logger
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from salver.facts import all_facts
from salver.common import models

from .base import BaseDB

__facts_index_mapping = [(fact, f'facts_{fact.lower()}') for fact in all_facts.keys()]


def fact_to_index(input_fact):
    for fact, index in __facts_index_mapping:
        if fact == input_fact:
            return index
    return None


def index_to_fact(input_index):
    for fact, index in __facts_index_mapping:
        if index == input_index:
            return fact
    return None


class ElasticsearchDB(BaseDB):
    def __init__(self, config):
        logger.info(f'elasticsearch: Build with {config}')
        self._client = Elasticsearch(hosts=[config.endpoint])

    def flush(self):
        logger.info(f'elasticsearch: Flush')
        for fact in all_facts.keys():
            index_name = fact_to_index(fact)
            self._client.indices.delete(index=index_name, ignore=[404])

    def bootstrap(self):
        logger.info(f'elasticsearch: Bootstrap')

    def add_facts(self, facts: List[models.BaseFact]):
        """Add facts."""
        logger.debug(f'elasticsearch: add {len(facts)}')

        def gen_actions(facts):
            for fact in facts:
                yield {
                    '_op_type': 'update',
                    '_index': fact_to_index(fact.schema()['title']),
                    '_id': fact.hash__,
                    'upsert': fact.dict(exclude={'hash__'}),
                    'doc': fact.dict(exclude={'first_seen', 'hash__'}),
                }

        bulk(client=self._client, actions=gen_actions(facts))

    def get_facts(self, facts_id: List[UUID]) -> List[models.BaseFact]:
        """Get facts by IDs."""
        logger.debug(f'elasticsearch: Get {len(facts_id)}')
        facts = []
        for fact_type, ids in facts_id.items():
            logger.info(f'Get {len(ids)} facts {fact_type}')
            res = self._client.mget(index=fact_to_index(fact_type), body={'ids': ids})
            for doc in res['docs']:
                facts.append(
                    models.BaseFact.from_obj(
                        fact_type=index_to_fact(doc['_index']),
                        data=doc['_source'],
                    ),
                )
        return facts