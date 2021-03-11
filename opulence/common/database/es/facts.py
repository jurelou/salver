from typing import List
from uuid import uuid4

from elasticsearch.helpers import bulk
from loguru import logger

from opulence.common.fact import BaseFact
from opulence.facts import all_facts

replicas = 0
refresh_interval = "3s"

__facts_index_mapping = [(fact, f"facts_{fact.lower()}") for fact in all_facts.keys()]
fact_to_index = lambda fact: [i for f, i in __facts_index_mapping if f == fact][0]
index_to_fact = lambda index: [f for f, i in __facts_index_mapping if i == index][0]


# def _refresh_indexes(client):
#     indexes = ";".join([ gen_index_name(fact) for fact in all_facts.keys() ])
#     print("@@@@", indexes)

#     client.indices.refresh(index=indexes, allow_no_indices=True)


def create_indexes(client):
    for fact, body in all_facts.items():
        index_name = fact_to_index(fact)
        logger.info(f"Create index {index_name}")
        client.indices.create(
            index=index_name, body=body.elastic_mapping(), ignore=400,
        )
        client.indices.put_settings(
            index=index_name,
            body={"refresh_interval": refresh_interval, "number_of_replicas": replicas},
        )


def remove_indexes(client):
    for fact in all_facts.keys():
        index_name = fact_to_index(fact)
        logger.info(f"Remove index {index_name}")
        client.indices.delete(index=index_name, ignore=[404])


def get_many(client, facts):
    mapping = {}
    for fact_type, fact_id in facts:
        if fact_type not in mapping:
            mapping[fact_type] = [fact_id]
        else:
            mapping[fact_type].append(fact_id)

    facts = []
    for fact_type, ids in mapping.items():
        logger.info(f"Get {fact_type}: {ids}")
        res = client.mget(index=fact_to_index(fact_type), body={"ids": ids})
        facts.extend(
            [
                BaseFact.from_obj(
                    fact_type=index_to_fact(doc["_index"]), data=doc["_source"],
                )
                for doc in res["docs"]
            ],
        )
    return facts


def bulk_upsert(client, facts):
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

    bulk(client=client, actions=gen_actions(facts))
