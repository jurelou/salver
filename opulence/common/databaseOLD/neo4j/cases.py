from uuid import uuid4

from loguru import logger

from opulence.common.models.case import Case
from opulence.common.models.scan import Scan


def create(client, case: Case):
    logger.info(f"Create case {case}")
    with client.session() as session:
        session.run(
            "CREATE (case: Case {external_id: $external_id}) " "SET case += $data",
            external_id=case.external_id.hex,
            data=case.dict(exclude={"external_id"}),
        )


def add_scan(client, case_id: uuid4, scan_id: uuid4):
    logger.info(f"Add case {case_id} to scan {scan_id}")
    with client.session() as session:
        session.run(
            "MATCH (case: Case), (scan: Scan) "
            "WHERE case.external_id = $case_external_id AND scan.external_id = $scan_external_id "
            "CREATE (case)-[r:LAUNCHES {name: 'yes'}]->(scan)",
            case_external_id=case_id.hex,
            scan_external_id=scan_id.hex,
        )
