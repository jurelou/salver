# -*- coding: utf-8 -*-
from salver.common.celery import async_call
from salver.controller.app import celery_app, db_manager
from salver.controller import tasks


#from salver.common.models.case import Case
#from salver.common.models.scan import Scan

from salver.facts import Company
from salver.facts import Domain
from salver.facts import Person
from salver.facts import Phone
from salver.facts import Username
from salver.facts import Email
import uuid

from salver.common.json_encoder import json_loads, json_dumps

from salver.controller import models
from salver.controller.services.database import exceptions
import sys


print("=====================================")
print("=     list collectors")
print("=====================================")

a = tasks.list_agents.delay()
res = a.get()
print("====res", res, type(res))
sys.exit(0)

print("=====================================")
print("=     PING")
print("=====================================")

a = tasks.ping.delay() #send_task()
res = a.get_leaf()
print("====PING RESULT", res, type(res))

print("=====================================")
print("=     create case 1")
print("=====================================")

case =  models.CaseInRequest(
        name="my-case1"
        )
try:
    case_id = tasks.create_case.delay(case)
    case1_id = case_id.get_leaf()
    print("CASE ID", case1_id, type(case1_id))
except exceptions.CaseAlreadyExists as err:
    print("CASE ALREADY EXISTS")

print("=====================================")
print("=     create case 2")
print("=====================================")
case2 =  models.CaseInRequest(
        name="my-case2"
        )
try:
    case_id = tasks.create_case.delay(case2)
    case2_id = case_id.get_leaf()
    print("CASE ID", case2_id, type(case2_id))
except exceptions.CaseAlreadyExists as err:
    print("CASE ALREADY EXISTS")



print("=====================================")
print("=     get case 2")
print("=====================================")

try:
    c = tasks.get_case.delay(case2_id.id)
    c = c.get()
    print("GET CASE", c)
except exceptions.CaseNotFound as err:
    pass

print("=====================================")
print("=     create scan 1")
print("=====================================")


scan = models.ScanInRequest(
        case_id=case1_id.id,
        facts=[Email(address="scan1")],
        scan_type="single_collector",
        config=models.ScanConfig(collector_name="dummy-collector")
)

try:
    res = tasks.create_scan.delay(scan)
    scan1 = res.get()
    print("CREATE SCAN", scan1)
except exceptions.CaseNotFound as err:
    print("=>", err)

print("=====================================")
print("=     create scan 2")
print("=====================================")


scan = models.ScanInRequest(
        case_id=case1_id.id,
        facts=[
            Person(firstname="1st", lastname="last"),
            Phone(number="+33123123"),
            Phone(number="+33689181869"),
            Username(name="jurelou"),
            Company(name="wavely"),
            Domain(fqdn="wavely.fr"),
            Person(
                firstname="fname",
                lastname="lname",
                anther="ldm",
                first_seen=42,
                last_seen=200,
            ),
            Email(address="test@gmail.test"),
            ],
        scan_type="single_collector",
        config=models.ScanConfig(collector_name="dummy-docker-collector")
)

try:
    res = tasks.create_scan.delay(scan)
    scan2 = res.get()
    print("CREATE SCAN", scan2)
except exceptions.CaseNotFound as err:
    print("=>", err)


print("=====================================")
print("=     launch scan 1")
print("=====================================")

from salver.controller.exceptions import InvalidScanConfiguration

try:
    res = tasks.launch_scan.delay(scan1.id)
    res = res.get()
    print("LAUNCH", res)
except exceptions.ScanNotFound as err:
    print("SCAN NOT FOUND", err)
except InvalidScanConfiguration as err:
    print("errrrrINVALID ONCIF", err)



print("=====================================")
print("=     launch scan 2")
print("=====================================")

from salver.controller.exceptions import InvalidScanConfiguration

try:
    res = tasks.launch_scan.delay(scan2.id)
    res = res.get()
    print("LAUNCH", res)
except exceptions.ScanNotFound as err:
    print("SCAN NOT FOUND", err)
except InvalidScanConfiguration as err:
    print("errrrrINVALID ONCIF", err)



print("=====================================")
print("=     get scan 1")
print("=====================================")

try:
    res = tasks.get_scan.delay(scan1.id)
    s = res.get()
    print(f"GET SCAN {type(s)} {s}")
    
except exceptions.ScanNotFound as err:
    print("NF", err)

print("=====================================")
print("=     get case 1")
print("=====================================")

try:
    c = tasks.get_case.delay(case1_id.id)
    c = c.get()
    print("GET CASE 1", c)
except exceptions.CaseNotFound as err:
    pass


tasks.reload_agents.delay().get()
# case = Case(name="tata")

# # db_manager.flush()
# scan = Scan(
#      case_id=case.external_id,
#      facts=[
#          Phone(number="+33123123"),
#          Phone(number="+33689181869"),
#          Username(name="jurelou"),
#          Company(name="wavely"),
#          Domain(fqdn="wavely.fr"),
#          Person(
#              firstname="fname",
#              lastname="lname",
#              anther="ldm",
#              first_seen=42,
#              last_seen=200,
#          ),
#          Email(address="test@gmail.test"),
#      ],
#      scan_type="single_collector",
#      config={"collector_name": "dummy-collector"},
# )


# a = db_manager.add_case(case)
# a = db_manager.add_scan(scan)

# toto = db_manager.get_scan(scan.external_id)

# task = async_call(
#     celery_app, "salver.controller.tasks.launch_scan", args=[scan.external_id],
# )
# print(task.get())


# task = async_call(celery_app, "salver.engine.tasks.test")


# print(task.get())
