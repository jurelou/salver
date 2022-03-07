# -*- coding: utf-8 -*-
import argparse

from opensearchpy import OpenSearch

from salver.common.facts import all_facts

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=('admin', 'admin'),
    use_ssl = True,
    verify_certs = False
)
replicas = 0
refresh_interval = "5s"


def create_es_mappings():
    for fact, body in all_facts.items():
        index_name = f"salver-facts-{fact.lower()}-*"
        mapping = body.elastic_mapping()

        template = {
            "settings": {
                "index": {
                "number_of_shards": 2,
                "number_of_replicas": 1
                }
            },
            **mapping
        }
        try:
            res = client.indices.create(fact.lower(), body=template)
            print(f"Create index {index_name}: {res}")
        except Exception as err:
            print("NOPE : ", err)

def flush_es_mappings():
    for fact in all_facts.keys():
        index_name = f"fact_{fact.lower()}*"
        res = client.indices.delete_index_template(name=index_name, ignore=[404])
        print(f"Remove index {index_name}: {res}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--remove",
        help="Remove elasticsearch mapping.",
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.remove:
        flush_es_mappings()
    else:
        create_es_mappings()
