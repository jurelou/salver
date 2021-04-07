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


from salver.common.json_encoder import json_loads, json_dumps



a = tasks.ping.delay() #send_task()
res = a.get_leaf()
print("====", res, type(res)) 


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
