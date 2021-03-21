# -*- coding: utf-8 -*-
from opulence.engine import tasks
from opulence.common import models
import pytest
from opulence.facts.username import Username
from opulence.engine.database import exceptions as db_exceptions
from opulence.engine import exceptions as engine_exceptions


@pytest.mark.usefixtures("engine_app", "database_manager")
class TestEngineTasks:
    def test_launch_scan(self):
        case = models.Case(name="test_engine_case_10")
        scan = models.Scan(
            case_id=case.external_id,
            facts=[Username(name="test username")],
            scan_type="single_collector",
            config={"collector_name": "some-collector"},
        )
        self.database_manager.add_case(case)
        self.database_manager.add_scan(scan)

        with pytest.raises(engine_exceptions.CollectorNotFound):
            tasks.launch_scan.s(scan.external_id).apply()

        # with pytest.raises(exceptions.ScanNotFound):
        #     tasks.launch_scan.s(1).apply()

    def test_launch_invalid_scan(self):
        with pytest.raises(db_exceptions.ScanNotFound):
            tasks.launch_scan.s(1).apply()
