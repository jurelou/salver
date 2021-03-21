# -*- coding: utf-8 -*-
# import pytest


# from opulence.engine.app
# class TestDatabaseManager:


#     def test_toto(self, celery_session_worker):
#         print("ok")
#         assert 1 == 1


# from opulence.engine import tasks
from opulence.common import models
import pytest
from opulence.facts.email import Email
from opulence.engine import tasks
import time

from mock import patch


@pytest.mark.usefixtures("agent_worker", "database_manager")
class TestAZeaze:
    def test_launch_scan_00(self):
        tasks.reload_agents()

        case = models.Case(name="test_scans_00")
        scan = models.Scan(
            case_id=case.external_id,
            facts=[Email(address="test_integration_scan_00")],
            scan_type="single_collector",
            config={"collector_name": "dummy-collector"},
        )
        self.database_manager.add_case(case)
        self.database_manager.add_scan(scan)

        tasks.launch_scan(scan.external_id)
        time.sleep(1.5)
        scan_db = self.database_manager.get_scan(scan.external_id)
        assert scan_db.state == models.ScanState.FINISHED
        assert scan_db.case_id == case.external_id
        assert scan_db.external_id == scan.external_id
        assert scan_db.scan_type == "single_collector"

    def test_launch_scan_01(self):
        tasks.reload_agents()

        case = models.Case(name="test_scans_01")
        scan = models.Scan(
            case_id=case.external_id,
            facts=[Email(address="test_integration_scan_01")],
            scan_type="single_collector",
            config={"collector_name": "dummy-collector"},
        )
        self.database_manager.add_case(case)
        self.database_manager.add_scan(scan)

        tasks.launch_scan(scan.external_id)
        time.sleep(2.5)
        scan_db = self.database_manager.get_scan(scan.external_id)
        assert scan_db.state == models.ScanState.FINISHED
        assert scan_db.case_id == case.external_id
        assert scan_db.external_id == scan.external_id
        assert scan_db.scan_type == "single_collector"
