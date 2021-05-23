# -*- coding: utf-8 -*-
import argparse

from elasticsearch import Elasticsearch

from salver.common.facts import all_facts

client = Elasticsearch(hosts=['localhost:9200'])
replicas = 0
refresh_interval = '5s'


def create_es_mappings():
    for fact, body in all_facts.items():
        index_name = f"facts_{fact.lower()}*"
        mapping = body.elastic_mapping()

        template = {
            "index_patterns": [index_name],
            "priority": 500,
            "_meta": {
                "description": f"Fact {fact}"
            },
            "template": {
                "settings": {
                    'refresh_interval': refresh_interval,
                    'number_of_replicas': replicas,
                },
                **mapping
            },
        }
        res = client.indices.put_index_template(
            name=fact.lower(),
            body=template,
        )
        print(f'Create index {index_name}: {res}')


def flush_es_mappings():
    for fact in all_facts.keys():
        index_name = f"fact_{fact.lower()}*"
        res = client.indices.delete_index_template(name=index_name, ignore=[404])
        print(f'Remove index {index_name}: {res}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--remove',
        help='Remove elasticsearch mapping.',
        action='store_true',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.remove:
        flush_es_mappings()
    else:
        create_es_mappings()