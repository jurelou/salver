# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from loguru import logger
from opulence.engine.database.base import BaseDB
from opulence.common import models
import httpx
from opulence.facts import all_facts
from typing import List
from elasticsearch.helpers import bulk

__facts_index_mapping = [(fact, f"facts_{fact.lower()}") for fact in all_facts.keys()]
fact_to_index = lambda fact: [i for f, i in __facts_index_mapping if f == fact][0]
index_to_fact = lambda index: [f for f, i in __facts_index_mapping if i == index][0]


class ElasticsearchDB(BaseDB):
    def __init__(self, config):
        print(f"Build elastic with {config}")
        self._client = Elasticsearch(hosts=[config.endpoint])

        self._kibana_endpoint = config.kibana_endpoint
        self._replicas = 0
        self._refresh_interval = "3s"

        self._kibana_index_patterns = ["facts_*"]
        self._kibana_index_patterns.extend(
            [fact_to_index(index) for index in all_facts.keys()],
        )

    def flush(self):
        self.flush_facts_indexes()
        # self.flush_kibana_patterns()

    def bootstrap(self):
        self.create_facts_indexes()
        self.create_kibana_patterns()

    def create_kibana_patterns(self):
        body = [
            {
                "type": "index-pattern",
                "id": index,
                "attributes": {"title": f"Fact {index}",},
            }
            for index in self._kibana_index_patterns
        ]

        kibana_endpoint = f"{self._kibana_endpoint}/api/saved_objects/_bulk_create"
        headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
        r = httpx.post(kibana_endpoint, json=body, headers=headers)
        logger.info(f"Create kibana index patterns: {r.status_code}")

    def flush_facts_indexes(self):
        for fact in all_facts.keys():
            index_name = fact_to_index(fact)
            logger.info(f"Remove index {index_name}")
            self._client.indices.delete(index=index_name, ignore=[404])

    def create_facts_indexes(self):
        for fact, body in all_facts.items():
            index_name = fact_to_index(fact)
            logger.info(f"Create index {index_name}")
            self._client.indices.create(
                index=index_name, body=body.elastic_mapping(), ignore=400,
            )
            self._client.indices.put_settings(
                index=index_name,
                body={
                    "refresh_interval": self._refresh_interval,
                    "number_of_replicas": self._replicas,
                },
            )

    def flush_kibana_patterns(self):
        def _delete_index(index_pattern):
            kibana_endpoint = f"{self._kibana_endpoint}/api/saved_objects/index-pattern/{index_pattern}"
            r = httpx.delete(kibana_endpoint, headers={"kbn-xsrf": "yes"})
            logger.info(f"Delete kibana index pattern {index_pattern}: {r.status_code}")

        [_delete_index(index) for index in self._kibana_index_patterns]

    def add_facts(self, facts: List[models.BaseFact]):
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

    def get_facts(self, facts):
        for fact_type, ids in facts.items():
            logger.info(f"Get {len(ids)} facts{fact_type}")
            res = self._client.mget(index=fact_to_index(fact_type), body={"ids": ids})
            for doc in res["docs"]:
                yield models.BaseFact.from_obj(
                    fact_type=index_to_fact(doc["_index"]), data=doc["_source"],
                )
