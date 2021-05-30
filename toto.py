# -*- coding: utf-8 -*-

from salver.common.kafka import Producer
from salver.common import models
from salver.config import engine_config
from salver.facts import *

# p = Person(firstname='1', lastname='1')
# p2 = Person(firstname='1', lastname='2')

# e = Email(address='addr')
# c = models.Collect(collector_name='dummy-collector', facts=[p, e, p2])
<<<<<<< HEAD
schema_registry = 'http://localhost:8081'
kafka_bootstrap = 'localhost:9092'


scan_producer = Producer(
    topic=f'scan-create',
=======
schema_registry = "http://localhost:8081"
kafka_bootstrap = "localhost:9092"


scan_producer = Producer(
    topic=f"scan",
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
    value_serializer=models.Scan,
    schema_registry_url=schema_registry,
    kafka_config = {
        'bootstrap.servers': kafka_bootstrap,
<<<<<<< HEAD
    },
)

s = models.Scan(
    scan_type='single-collector',
    config=models.ScanConfig(collector_name='dummy-docker-collector'),
    facts=[

                Phone(number='+33689181869'),
                Username(name='jurelou'),
                Company(name='wavely'),
                Domain(fqdn='wavely.fr'),
                Person(
                    firstname='fname',
                    lastname='lname',
                    anther='ldm',
                    first_seen=42,
                    last_seen=200,
                ),
                Email(address='test@gmail.test'),
    ],
)

# s = models.Scan(
#     scan_type='full-scan',
#     config=models.ScanConfig(collector_name='dummy-docker-collector'),
#     facts=[

#                 Phone(number='+33689181869'),
#                 Username(name='jurelou'),
#                 Company(name='wavely'),
#                 Domain(fqdn='wavely.fr'),
#                 Person(
#                     firstname='fname',
#                     lastname='lname',
#                     anther='ldm',
#                     first_seen=42,
#                     last_seen=200,
#                 ),
#                 Email(address='test@gmail.test'),
#     ],
# )

=======
    }
)


s = models.Scan(
    scan_type="full-scan",
    config=models.ScanConfig(collector_name="dummy-docker-collector"),
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
)

>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
scan_producer.produce(s, flush=True)
