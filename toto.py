# -*- coding: utf-8 -*-
from opulence.common.celery import async_call
from opulence.engine.app import celery_app, db_manager


from opulence.common.models.case import Case
from opulence.common.models.scan import Scan

from opulence.facts.company import Company
from opulence.facts.domain import Domain
from opulence.facts.person import Person
from opulence.facts.phone import Phone
from opulence.facts.username import Username
from opulence.facts.email import Email

case = Case(name="tata")

db_manager.flush()
scan = Scan(
    case_id=case.external_id,
    facts=[
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
    config={"collector_name": "dummy-collector"},
)


a = db_manager.add_case(case)
a = db_manager.add_scan(scan)

toto = db_manager.get_scan(scan.external_id)

task = async_call(
    celery_app, "opulence.engine.tasks.launch_scan", args=[scan.external_id],
)
print(task.get())


# task = async_call(celery_app, "opulence.engine.tasks.test")

# print(task.get())
