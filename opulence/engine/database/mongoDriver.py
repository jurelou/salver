from dynaconf import settings
from mongoengine import connect

from opulence.common.job import StatusCode
from opulence.common.utils import now

from . import mongoModels as models


class Collectors:
    def __init__(self, client):
        self.client = client

    def get(self):
        return models.Collector.objects()

    def get_by_id(self, identifier):
        return models.Collector.objects(external_identifier=identifier).first()

    def update_by_id(self, identifier, data):
        return models.Collector(external_identifier=identifier, **data).save()

    def flush(self):
        return models.Collector.objects.delete()

    def find_by_allowed_input(self, input_fact):
        collectors = self.get()
        result = []
        for collector in collectors:
            if any(
                ai["plugin_data"]["name"] == input_fact
                for ai in collector.allowed_input
            ):
                result.append(collector.external_identifier)
        return result


class CollectorResults:
    def __init__(self, client):
        self.client = client

    def get_by_id(self, identifier):
        return models.Collector_result.objects(identifier=identifier).first()


class Results:
    def __init__(self, client):
        self.client = client

    def get_by_scan_id(self, scan_id):
        return models.Result.objects(scan_identifier=scan_id)[
            :settings.DB_QUERY_LIMIT.mongo_objects]

    def get_by_id(self, identifier):
        return models.Result.objects(identifier=identifier)

    def add_many(self, scan_id, results):

        # TODO: Refactor this
        if results["status"][0] >= 100:
            models.Scan(external_identifier=scan_id).update(
                set__status=results["status"]
            )
        models.Scan(external_identifier=scan_id).update(inc__stats__number_of_results=1)

        for result in results["output"]:
            models.Result(
                scan_identifier=scan_id,
                result_identifier=results["identifier"],
                **result
            ).save()

        results.pop("output", None)
        models.Collector_result(scan_identifier=scan_id, **results).save()


class Scans:
    def __init__(self, client):
        self.client = client

    def create_or_update(self, scan_name, data):
        return models.Scan(
            external_identifier=scan_name,
            status=(StatusCode.started, ""),
            stats=models.Stats(),
            **data
        ).save()

    def get(self):
        return models.Scan.objects()

    def stop(self, scan_id):
        scan = self.get_by_id(scan_id).get()
        if not scan.status[0] >= 100:
            return models.Scan(external_identifier=scan_id).update(
                set__status=(40, ""), set__stats__end_date=now()
            )

        return models.Scan(external_identifier=scan_id).update(
            set__stats__end_date=now()
        )

    def get_by_id(self, identifier):
        return models.Scan.objects(external_identifier=identifier)

    def flush(self):
        models.Collector_result.objects.delete()
        models.Result.objects.delete()
        models.Scan.objects.delete()

    def delete_by_id(self, identifier):
        models.Collector_result.objects(scan_identifier=identifier).delete()
        # models.Result.objects(scan_identifier=identifier).delete()
        return models.Scan.objects(external_identifier=identifier).delete()


class Facts:
    def __init__(self, client):
        self.client = client

    def get(self):
        return models.Fact.objects()

    def get_by_id(self, identifier):
        return models.Fact.objects(external_identifier=identifier)

    def get_by_name(self, name):
        return models.Fact.objects(plugin_data__name=name).first()

    def update_by_id(self, identifier, data):
        return models.Fact(external_identifier=identifier, **data).save()

    def flush(self):
        return models.Fact.objects.delete()


class MongoDriver:
    def __init__(self):
        config = settings.MONGO
        client = connect(
            config["database"],
            host=config["url"],
            serverSelectionTimeoutMS=config["connect_timeout"],
        )
        self.facts = Facts(client)
        self.scans = Scans(client)
        self.results = Results(client)
        self.collectors = Collectors(client)
        self.collector_results = CollectorResults(client)
