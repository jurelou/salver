# -*- coding: utf-8 -*-
import argparse

from elasticsearch import Elasticsearch

<<<<<<< HEAD
from salver.common import models
=======
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
from salver.common.facts import all_facts

client = Elasticsearch(hosts=['localhost:9200'])
replicas = 0
refresh_interval = '5s'


<<<<<<< HEAD
def _create_index(name, index_pattern, mapping):

    template = {
        'index_patterns': [index_pattern],
        'priority': 500,
        '_meta': {'description': name},
        'template': {
            'settings': {
                'refresh_interval': refresh_interval,
                'number_of_replicas': replicas,
            },
            **mapping,
        },
    }
    res = client.indices.put_index_template(
        name=name,
        body=template,
    )
    print(f'Create index {name}: {res}')


def create_es_mappings():
    _create_index('error', 'error-*', models.Error.elastic_mapping())
    _create_index(
        'collect-done',
        'collect-done-*',
        models.CollectDone.elastic_mapping(),
    )

    for fact, body in all_facts.items():
        index_name = f'facts_{fact.lower()}-*'
        mapping = body.elastic_mapping()
        _create_index(fact.lower(), index_name, mapping)
=======
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
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96


def flush_es_mappings():
    for fact in all_facts.keys():
<<<<<<< HEAD
        index_name = f'fact_{fact.lower()}*'
=======
        index_name = f"fact_{fact.lower()}*"
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
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
<<<<<<< HEAD
        create_es_mappings()
=======
        create_es_mappings()
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
