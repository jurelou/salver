import argparse

from elasticsearch import Elasticsearch

from salver.facts import all_facts
from salver.common.database.elasticsearch import fact_to_index, index_to_fact

client = Elasticsearch(hosts=["localhost:9200"])
replicas = 0
refresh_interval = "5s"


def create_es_mappings():
    for fact, body in all_facts.items():
        index_name = fact_to_index(fact)
        mapping = body.elastic_mapping()
        mapping["settings"] = {
            "refresh_interval": refresh_interval,
            "number_of_replicas": replicas,
        }

        res = client.indices.put_index_template(
            name=index_name,
            body={"index_patterns": index_name + "*", "template": mapping},
        )
        print(f"Create index {index_name}: {res}")


def flush_es_mappings():
    for fact in all_facts.keys():
        index_name = fact_to_index(fact)
        res = client.indices.delete_index_template(name=index_name, ignore=[404])
        print(f"Remove index {index_name}: {res}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--remove", help="Remove elasticsearch mapping.", action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.remove:
        flush_es_mappings()
    else:
        create_es_mappings()
