#-*- coding: utf-8 -*-
from opulence.engine import tasks
from opulence.common import models
import pytest
from opulence.facts.username import Username
from opulence.engine.database import exceptions as db_exceptions
from opulence.engine import exceptions as engine_exceptions



from opulence.engine.tasks import launch_scan
from mock import patch


@pytest.mark.usefixtures("engine_app", "database_manager")
class TestScans:

    @patch("opulence.engine.scans.base.get_agents")
    def test_launch_scan_00(self, mock_get_agents):
        mock_get_agents.return_value = {"any": ["dummy-collector"]}

        case = models.Case(name="test_scans_00")
        scan = models.Scan(
            case_id=case.external_id,
            facts=[
                Username(name="test username")
            ],
            scan_type="single_collector",
            config={"collector_name": "dummy-collector"},
        )
        self.database_manager.add_case(case)
        self.database_manager.add_scan(scan)
        scan_in_db = self.database_manager.get_scan(scan.external_id)
        assert scan_in_db.state == "created"

        launch_scan(scan.external_id)

        scan_in_db = self.database_manager.get_scan(scan.external_id)
        assert scan_in_db.state == "started"

    def test_launch_scan_01(self):

        case = models.Case(name="test_scans_01")
        scan = models.Scan(
            case_id=case.external_id,
            facts=[
                Username(name="test username")
            ],
            scan_type="single_collector",
            config={"collector_name": "dummy-collector"},
        )
        self.database_manager.add_case(case)
        self.database_manager.add_scan(scan)

        with pytest.raises(engine_exceptions.CollectorNotFound):
            launch_scan(scan.external_id)

