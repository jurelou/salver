# -*- coding: utf-8 -*-
import argparse

import httpx

from salver.common.facts import all_facts

kibana_url = "http://localhost:5601"
kibana_index_patterns = ["facts_*", "error*"]
kibana_index_patterns.extend([f"fact_{fact.lower()}*" for fact in all_facts.keys()])


def create_kibana_patterns(patterns):
    body = [
        {"type": "index-pattern", "id": pattern, "attributes": {"title": pattern}}
        for pattern in patterns
    ]

    kibana_endpoint = f"{kibana_url}/api/saved_objects/_bulk_create"
    headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
    r = httpx.post(kibana_endpoint, json=body, headers=headers)
    print(f"Create kibana index patterns: {r.status_code}, {r}")


def flush_kibana_patterns(patterns):
    def _delete_index(pattern):
        kibana_endpoint = f"{kibana_url}/api/saved_objects/index-pattern/{pattern}"
        r = httpx.delete(kibana_endpoint, headers={"kbn-xsrf": "yes"})
        print(f"Delete kibana index pattern {pattern}: {r.status_code}")

    [_delete_index(index) for index in patterns]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--remove",
        help="Remove kibana index patterns.",
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.remove:
        flush_kibana_patterns(kibana_index_patterns)
    else:
        create_kibana_patterns(kibana_index_patterns)
