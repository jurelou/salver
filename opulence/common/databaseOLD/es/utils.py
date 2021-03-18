# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import httpx
from loguru import logger

from opulence.common.database.es import facts
from opulence.facts import all_facts

kibana_index_patterns = ["facts_*"]
kibana_index_patterns.extend(
    [facts.fact_to_index(index) for index in all_facts.keys()],
)


def create_client(config):
    logger.info(f"Create elasticsearch client: {config.endpoint}")
    return Elasticsearch(hosts=[config.endpoint])


def create_indexes(es_client):
    facts.create_indexes(es_client)


def remove_indexes(es_client):
    logger.warning("Flush elasticsearch indexes")
    facts.remove_indexes(es_client)


def create_kibana_patterns(es_client, kibana_url):
    def _create_index(index_pattern):
        kibana_endpoint = (
            f"{kibana_url}/api/saved_objects/index-pattern/{index_pattern}"
        )
        headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
        data = {
            "attributes": {"title": index_pattern},
        }
        r = httpx.post(kibana_endpoint, json=data, headers=headers)
        logger.info(f"Create kibana index pattern {index_pattern}: {r.status_code}")

    [_create_index(index) for index in kibana_index_patterns]


def remove_kibana_patterns(es_client, kibana_url):
    def _delete_index(index_pattern):
        kibana_endpoint = (
            f"{kibana_url}/api/saved_objects/index-pattern/{index_pattern}"
        )
        r = httpx.delete(kibana_endpoint, headers={"kbn-xsrf": "yes"})
        logger.info(f"Delete kibana index pattern {index_pattern}: {r.status_code}")

    [_delete_index(index) for index in kibana_index_patterns]
