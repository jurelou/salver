# -*- coding: utf-8 -*-
from opulence.engine.database.manager import DatabaseManager
from opulence.common import models
import pytest
from uuid import uuid4
from opulence.facts.username import Username


@pytest.mark.usefixtures("database_manager")
class TestDatabaseManager:
    def test_create_case(self):
        case = models.Case(name="test_case")
        self.database_manager.add_case(case)
        case_in_db = self.database_manager.get_case(case.external_id)
        assert case == case_in_db

    def test_create_scan_invalid_case(self):

        scan = models.Scan(
            case_id=uuid4(),
            facts=[Username(name="test username"),],
            scan_type="single_collector",
            config={},
        )

        a = self.database_manager.add_scan(scan)
        # case_in_db = self.database_manager.get_case(case.external_id)
        # assert case == case_in_db

        # from opulence.engine import tasks  # pragma: nocover

        # from opulence.common.models.case import Case
        # from opulence.common.models.scan import Scan

        # from opulence.facts.company import Company
        # from opulence.facts.domain import Domain
        # from opulence.facts.person import Person
        # from opulence.facts.phone import Phone
        # from opulence.facts.username import Username
        # from opulence.facts.email import Email

        # case = Case(name="tata")

        # scan = Scan(
        #     case_id=case.external_id,
        #     facts=[
        #         Phone(number="+33123123"),
        #         Phone(number="+33689181869"),
        #         Username(name="jurelou"),
        #         Company(name="wavely"),
        #         Domain(fqdn="wavely.fr"),
        #         Person(
        #             firstname="fname",
        #             lastname="lname",
        #             anther="ldm",
        #             first_seen=42,
        #             last_seen=200,
        #         ),
        #         Email(address="test@gmail.test"),
        #     ],
        #     scan_type="single_collector",
        #     config={"collector_name": "dummy-docker-collector"},
        # )
        # scan2 = Scan(
        #     case_id=case.external_id,
        #     facts=[Username(name="jurelou", something="else")],
        #     scan_type="single_collector",
        #     collector_name="dummy-docker-collector",
        #     config={},
        # )

        # a = db_manager.add_case(case)
        # a = db_manager.add_scan(scan)
        # db_manager.add_scan(scan2)

        # case = db_manager.get_scan(scan.external_id)
        # print("!!!!CASE", case)

        # tasks.launch_scan.apply(args=[scan.external_id])
