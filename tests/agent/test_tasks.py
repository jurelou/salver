# -*- coding: utf-8 -*-
from opulence.agent import tasks
from opulence.facts.person import Person
from opulence.facts.email import Email

from mock import patch
import pytest
from opulence.agent import exceptions


@pytest.mark.usefixtures("agent_app")
class TestScan:
    @patch("opulence.agent.tasks.current_task")
    def test_scan_00(self, mock):
        mock.request.delivery_info = {"routing_key": "dummy-collector"}
        res = tasks.scan.s([Email(address="test00")]).apply().get()

        assert res["executions_count"] == 1
        assert len(res["facts"]) == 2

    @patch("opulence.agent.tasks.current_task")
    def test_scan_01(self, mock):
        mock.request.delivery_info = {"routing_key": "dummy-docker-collector"}
        res = (
            tasks.scan.s(
                [
                    Email(address="test01"),
                    Person(firstname="test_firstname", lastname="test_lastname"),
                ],
            )
            .apply()
            .get()
        )

        assert res["executions_count"] == 2
        assert len(res["facts"]) == 4

    @patch("opulence.agent.tasks.current_task")
    def test_scan_02(self, mock):
        mock.request.delivery_info = {"routing_key": "dummy-collector"}
        res = (
            tasks.scan.s([Email(address="test02_a"), Email(address="test02_b")])
            .apply()
            .get()
        )

        assert res["executions_count"] == 2
        assert len(res["facts"]) == 4

    @patch("opulence.agent.tasks.current_task")
    def test_scan_100(self, mock):
        mock.request.delivery_info = {"routing_key": "thishouldnotexists"}
        p = Person(firstname="dummy_firstname", lastname="dummy_lastname")
        with pytest.raises(exceptions.CollectorNotFound):
            tasks.scan.s([p]).apply()
