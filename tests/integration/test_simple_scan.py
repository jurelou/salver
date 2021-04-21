# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from salver.api.main import app
from salver.common import models
from salver.api import models as api_models
import time
import sys
from tests import api
from salver.facts import Person

client = TestClient(app)
CASE_NAME = "simple scan case"


def test_simple_scan():
    # Creates a case
    case = models.Case(name=CASE_NAME)
    res = api.create_case(case)
    case_id = res["id"]

    # Check if the case have been created
    res = api.get_case(case_id)
    case = res["case"]
    assert case["name"] == CASE_NAME
    assert case["scans"] == []

    # Check if the case is present in the list of cases IDs
    res = api.get_all_cases(case_id)
    all_cases = res["ids"]
    assert case_id in all_cases

    # Adds a scan to our case
    scan = api_models.ScanInRequest(
        case_id=case_id,
        scan_type="single_collector",
        facts=[
            api_models.FactInRequest(
                fact_type="Person",
                fact=Person(
                    firstname="test-single-collector-firstname",
                    lastname="test-single-collector-firstname",
                ),
            ),
        ],
        config=models.ScanConfig(collector_name="dummy-docker-collector"),
    )
    res = api.create_scan(scan)
    scan_id = res["id"]

    # Check if the scan have been created
    scan = api.get_scan(scan_id)
    assert scan["case_id"] == case_id
    assert scan["scan_type"] == "single_collector"
    assert scan["state"] == "created"
    assert scan["external_id"] == scan_id
    assert len(scan["facts"]) == 1
    fact = scan["facts"][0]
    assert fact["fact_type"] == "Person"
    assert fact["firstname"] == "test-single-collector-firstname"
    assert fact["lastname"] == "test-single-collector-firstname"

    # Check if the case contains the scan ID
    res = api.get_case(case_id)
    case = res["case"]
    assert case["scans"] == [scan_id]

    # Launch the scan
    res = api.launch_scan(scan_id)
    assert res == "OK"

    # wait for the scan to finish
    time.sleep(2)

    # Check if the scan is in "finished" state
    scan = api.get_scan(scan_id)
    assert scan["state"] == "finished"
