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
import httpx

from salver.common.json_encoder import json_loads, json_dumps
from salver.common.models import ScanConfig, Case
from salver.controller import models
from salver.api import models as api_models
from salver.common.database import exceptions
import sys

API_ENDPOINT = "http://localhost:8000/api"


print("=====================================")
print("=     list collectors")
print("=====================================")

a = httpx.get(API_ENDPOINT + "/agents")
res = a.json()
assert a.status_code == 200

assert len(res["agents"]) == 1



a = tasks.list_agents.delay()
res = a.get()
print("====res", res, type(res))

print("=====================================")
print("=     PING")
print("=====================================")

a = tasks.ping.delay() #send_task()
res = a.get_leaf()
print("====PING RESULT", res, type(res))

print("=====================================")
print("=     create case 1")
print("=====================================")

case =  Case(
        name="my-case1" + uuid.uuid4().hex
        )
a = httpx.post(API_ENDPOINT + f"/cases", data=case.json())
print("!!!!", a.json(), a)
case1_id = a.json()
assert a.status_code == 200

"""
try:
    case_id = tasks.create_case.delay(case)
    case1_id = case_id.get_leaf()
    print("CASE ID", case1_id, type(case1_id))
except exceptions.CaseAlreadyExists as err:
    print("CASE ALREADY EXISTS")
"""


print("=====================================")
print("=     create case 2")
print("=====================================")

case2 =  Case(
        name="my-case2" + uuid.uuid4().hex
        )

a = httpx.post(API_ENDPOINT + f"/cases", data=case2.json())
assert a.status_code == 200

case2_id = a.json()
print(case2_id)


print("=====================================")
print("=     get case 2")
print("=====================================")
"""
try:
    c = tasks.get_case.delay(case2_id.id)
    c = c.get()
    print("GET CASE", c)
except exceptions.CaseNotFound as err:
    pass
"""

a = httpx.get(API_ENDPOINT + f"/cases/{case2_id['id']}")
assert a.status_code == 200

res = a.json()

print(res)


print("=====================================")
print("=     create scan 1")
print("=====================================")

scan = {
  "case_id": case1_id["id"],
  "facts": [
    {
      "fact_type": "Person",
      "fact": {
        "firstname": "aaaaaaJoazehn",
        "lastname": "bbbbbbDoe",
      }
    }
  ],
  "scan_type": "single_collector",
  "config": {
    "collector_name": "dummy-docker-collector"
  }
}

a = httpx.post(API_ENDPOINT + f"/scans", json=scan)
print(a.json())
scan_1 = a.json()["id"]
assert a.status_code == 200

print("=====================================")
print("=     create scan 2")
print("=====================================")


# scan = models.ScanInRequest(
#         case_id=case1_id["id"],
#         facts=[
#             Person(firstname="1st", lastname="last"),
#             Phone(number="+33123123"),
#             Phone(number="+33689181869"),
#             Username(name="jurelou"),
#             Company(name="wavely"),
#             Domain(fqdn="wavely.fr"),
#             Person(
#                 firstname="fname",
#                 lastname="lname",
#                 anther="ldm",
#                 first_seen=42,
#                 last_seen=200,
#             ),
#             Email(address="test@gmail.test"),
#             ],
#         scan_type="single_collector",
#         config=ScanConfig(collector_name="dummy-docker-collector")
# )

# try:
#     res = tasks.create_scan.delay(scan)
#     scan2 = res.get()
#     print("CREATE SCAN", scan2)
# except exceptions.CaseNotFound as err:
#     print("=>", err)


print("=====================================")
print("=     launch scan 1")
print("=====================================")

from salver.controller.exceptions import InvalidScanConfiguration

try:
    res = tasks.launch_scan.delay(uuid.UUID(scan_1))
    res = res.get()
    print("LAUNCH", res)
except exceptions.ScanNotFound as err:
    print("SCAN NOT FOUND", err)
except InvalidScanConfiguration as err:
    print("errrrrINVALID ONCIF", err)



print("=====================================")
print("=     launch scan 2")
print("=====================================")

# from salver.controller.exceptions import InvalidScanConfiguration

# try:
#     res = tasks.launch_scan.delay(scan2.id)
#     res = res.get()
#     print("LAUNCH", res)
# except exceptions.ScanNotFound as err:
#     print("SCAN NOT FOUND", err)
# except InvalidScanConfiguration as err:
#     print("errrrrINVALID ONCIF", err)



print("=====================================")
print("=     get scan 1")
print("=====================================")

"""
try:
    res = tasks.get_scan.delay(scan1.id)
    s = res.get()
    print(f"GET SCAN {type(s)} {s}")
    
except exceptions.ScanNotFound as err:
    print("NF", err)
"""

a = httpx.get(API_ENDPOINT + f"/scans/{scan_1}")
assert a.status_code == 200

res = a.json()
assert res["case_id"] == case1_id["id"]



print("=====================================")
print("=     get case 1")
print("=====================================")
"""
try:
    c = tasks.get_case.delay(case1_id.id)
    c = c.get()
    print("GET CASE 1", c)
except exceptions.CaseNotFound as err:
    pass
"""

a = httpx.get(API_ENDPOINT + f"/cases/{case1_id['id']}")
assert a.status_code == 200
assert a.json()["scans"][0] == scan_1
res = a.json()

print(res)


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
