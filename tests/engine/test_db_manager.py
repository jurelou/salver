# -*- coding: utf-8 -*-
from opulence.engine.database.manager import DatabaseManager
from opulence.common import models
import pytest
from uuid import uuid4
from opulence.facts.username import Username
from opulence.engine.database import exceptions


@pytest.mark.usefixtures("database_manager")
class TestDatabaseManager:
    def test_create_case(self):
        case = models.Case(name="test_db_case")
        self.database_manager.add_case(case)
        case_in_db = self.database_manager.get_case(case.external_id)
        assert case == case_in_db

    def test_create_scan(self):
        case = models.Case(name="test_db_case_01")
        scan = models.Scan(
            case_id=case.external_id,
            facts=[Username(name="test username")],
            scan_type="single_collector",
            config={},
        )
        self.database_manager.add_case(case)
        self.database_manager.add_scan(scan)

        new_scan = self.database_manager.get_scan(scan.external_id)
        assert new_scan.external_id == scan.external_id
        assert new_scan.case_id == case.external_id
        assert new_scan.facts[0].name == "test username"

    def test_create_scan_invalid_case(self):
        scan = models.Scan(
            case_id=uuid4(),
            facts=[Username(name="test username")],
            scan_type="single_collector",
            config={},
        )
        with pytest.raises(exceptions.CaseNotFound):
            self.database_manager.add_scan(scan)

    def test_get_invalid_case(self):
        invalid_uuid = uuid4()
        with pytest.raises(exceptions.CaseNotFound) as err:
            self.database_manager.get_case(invalid_uuid)
        assert str(invalid_uuid) in str(err.value)

    def test_get_invalid_scan(self):
        invalid_uuid = uuid4()
        with pytest.raises(exceptions.ScanNotFound) as err:
            self.database_manager.get_scan(invalid_uuid)
        assert str(invalid_uuid) in str(err.value)
