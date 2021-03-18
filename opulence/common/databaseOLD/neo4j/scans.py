# -*- coding: utf-8 -*-
from time import time
from typing import List
from uuid import uuid4

from loguru import logger

from opulence.common.models.scan import Scan


def get(client, scan_id: uuid4):
    with client.session() as session:
        result = session.run(
            "MATCH (scan: Scan) "
            "WHERE scan.external_id=$external_id "
            "RETURN DISTINCT scan",
            external_id=scan_id.hex,
        )
        scan = result.single()
        return Scan(**scan.data()["scan"])


def get_user_input_facts(client, scan_id: uuid4, include_scan=True):
    logger.info(f"Get user input facts from scan {scan_id}")
    with client.session() as session:
        result = session.run(
            "MATCH (scan: Scan)-[link:consists_of]->(fact: Fact) "
            "WHERE scan.external_id=$external_id "
            "RETURN DISTINCT fact",
            external_id=scan_id.hex,
        )
        data = result.data()

        return [(item["fact"]["type"], item["fact"]["external_id"]) for item in data]


def create(client, scan: Scan):
    logger.info(f"Create scan {scan}")
    with client.session() as session:
        session.run(
            "CREATE (scan:Scan {external_id: $external_id}) " "SET scan += $data",
            external_id=scan.external_id.hex,
            data=scan.dict(exclude={"external_id", "facts"}),
        )


def add_facts(
    client, scan_id: uuid4, facts_ids: List[str], relationship: str = "UNKNOWN",
):
    formated_links = [{"from": scan_id.hex, "to": fact} for fact in facts_ids]

    print(formated_links)
    logger.info(f"Add {len(facts_ids)} facts to {scan_id} with relation {relationship}")
    with client.session() as session:

        session.run(
            "UNWIND $links as link "
            "MATCH (from:Scan), (to:Fact) "
            "WHERE from.external_id = link.from AND to.external_id = link.to "
            "CALL apoc.create.relationship(from, $relationship, {ts: $timestamp}, to) "
            "YIELD rel "
            "RETURN rel ",
            links=formated_links,
            timestamp=time(),
            relationship=relationship,
        )
