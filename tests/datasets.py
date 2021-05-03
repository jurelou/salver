# -*- coding: utf-8 -*-
import uuid
from salver import facts
from salver.common import models
from salver.api import models as api_models
from tests import api

UNIT_CONTROLLER_SCAN_1 = None

def unit_controller():
    global UNIT_CONTROLLER_SCAN_1

    case = models.Case(name='test-unit-controller-tasks')
    case = api.create_case(case)

    scan = api_models.ScanInRequest(
        case_id=case['id'],
        scan_type='single_collector',
        facts=[
            api_models.FactInRequest(
                fact_type='Person',
                fact=facts.Person(
                    firstname='test-unit-controller-tasks-fname',
                    lastname='test-unit-controller-tasks-lname',
                ),
            ),
        ],
        config=models.ScanConfig(collector_name='dummy-docker-collector'),
    )
    scan = api.create_scan(scan)
    UNIT_CONTROLLER_SCAN_1 = uuid.UUID(scan['id'])

def boot():
    unit_controller()
