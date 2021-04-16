# -*- coding: utf-8 -*-
from typing import List

import httpx
from loguru import logger
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from salver.facts import all_facts
from salver.common import models

from .base import BaseDB

__facts_index_mapping = [(fact, f"facts_{fact.lower()}") for fact in all_facts.keys()]
fact_to_index = lambda fact: [i for f, i in __facts_index_mapping if f == fact][0]
index_to_fact = lambda index: [f for f, i in __facts_index_mapping if i == index][0]


class ElasticsearchDB(BaseDB):
    def __init__(self, config):
        print(f"Build elastic with {config}")
        self._client = Elasticsearch(hosts=[config.endpoint])

    def flush(self):
        for fact in all_facts.keys():
            index_name = fact_to_index(fact)
            logger.info(f"Remove index {index_name}")
            self._client.indices.delete(index=index_name, ignore=[404])

    def bootstrap(self):
        pass

    def add_facts(self, facts: List[models.BaseFact]):
        print("ADD FACTS", facts)

        def gen_actions(facts):
            for fact in facts:
                yield {
                    "_op_type": "update",
                    "_index": fact_to_index(fact.schema()["title"]),
                    "_id": fact.hash__,
                    "upsert": fact.dict(exclude={"hash__"}),
                    "doc": fact.dict(exclude={"first_seen", "hash__"}),
                }

        bulk(client=self._client, actions=gen_actions(facts))

    def get_facts(self, facts_id) -> List[models.BaseFact]:
        facts = []
        for fact_type, ids in facts_id.items():
            logger.info(f"Get {len(ids)} facts {fact_type}")
            res = self._client.mget(index=fact_to_index(fact_type), body={"ids": ids})
            for doc in res["docs"]:
                facts.append(
                    models.BaseFact.from_obj(
                        fact_type=index_to_fact(doc["_index"]),
                        data=doc["_source"],
                    )
                )
        return facts
