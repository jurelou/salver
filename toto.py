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


a = tasks.ping.delay() #send_task()
res = a.get_leaf()
print("====PING RESULT", res, type(res))

print("=====================================")

case =  models.CaseInRequest(
        name="my-casei" + uuid.uuid4().hex
        )
try:
    case_id = tasks.create_case.delay(case)
    print("aaa", case_id, type(case_id))
    case_id = case_id.get_leaf()
    print("CASE ID", case_id, type(case_id))
except exceptions.CaseAlreadyExists as err:
    print("CASE ALREADY EXISTS")

print("=====================================")
try:
    c = tasks.get_case.delay(case_id.id)
    c = c.get()
    print("GET CASE", c)
except exceptions.CaseNotFound as err:
    pass


print("=====================================")




scan = models.ScanInRequest(
        case_id=case_id.id,
        facts=[Person(firstname="1st", lastname="last")],
        scan_type="myscan",
        config=models.ScanConfig(a="aa")
)

try:
    res = tasks.create_scan.delay(scan)
    s = res.get()
    print("CREATE SCAN", s)
except exceptions.CaseNotFound as err:
    print("=>", err)

print("=====================================")

try:
    res = tasks.get_scan.delay(s.id)
    s = res.get()
    print(f"GET SCAN {type(s)} {s}")
    
except exceptions.ScanNotFound as err:
    print("NF", err)


print("=====================================")
try:
    c = tasks.get_case.delay(case_id.id)
    c = c.get_leaf()
    print("GET CASE", c)
except exceptions.CaseNotFound as err:
    pass
print("=====================================")




print("-------------------------------------")

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
