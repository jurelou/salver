from opulence.common.patterns import Singleton

from .mongoDriver import MongoDriver
from .neoDriver import NeoDriver


class Collectors:
    def __init__(self, mongo_driver):
        self.mongo_driver = mongo_driver

    def get(self):
        return self.mongo_driver.collectors.get()

    def get_by_id(self, identifier):
        return self.mongo_driver.collectors.get_by_id(identifier)

    def update_by_id(self, identifier, data):
        return self.mongo_driver.collectors.update_by_id(identifier, data)

    def flush(self):
        return self.mongo_driver.collectors.flush()

    def find_by_allowed_input(self, input_list):
        return self.mongo_driver.collectors.find_by_allowed_input(input_list)


class CollectorResults:
    def __init__(self, mongo_driver):
        self.mongo_driver = mongo_driver

    def get_by_id(self, identifier):
        return self.mongo_driver.collector_results.get_by_id(identifier)


class Results:
    def __init__(self, mongo_driver, neo_driver):
        self.mongo_driver = mongo_driver
        self.neo_driver = neo_driver

    def get_by_scan_id(self, scan_id):
        return self.mongo_driver.results.get_by_scan_id(scan_id)

    def get_node_by_value(self, value):
        return self.neo_driver.results.get_node_by_value(value)

    def get_by_id(self, identifier):
        return self.mongo_driver.results.get_by_id(identifier)

    def add_many(self, scan_id, results):
        print("Adding many results:", len(results["output"]))
        results["output"] = results["output"][:100]
        print("Sliced to:", len(results["output"]))
        self.neo_driver.results.add_many(results)
        self.mongo_driver.results.add_many(scan_id, results)


class Scans(object):
    def __init__(self, mongo_driver, neo_driver):
        self.mongo_driver = mongo_driver
        self.neo_driver = neo_driver

    def stop(self, scan_id):
        return self.mongo_driver.scans.stop(scan_id)

    def get(self):
        return self.mongo_driver.scans.get()

    def tree(self, scan_id):
        return self.neo_driver.scans.tree(scan_id)

    def create_or_update(self, scan_name, data):
        self.neo_driver.scans.create_or_update(scan_name, data)
        self.mongo_driver.scans.create_or_update(scan_name, data)

    def add_input(self, scan_id, input_id):
        self.neo_driver.scans.add_input(scan_id, input_id)

    def add_result(self, scan_id, input_id):
        self.neo_driver.scans.add_input(scan_id, input_id)

    def flush(self):
        self.mongo_driver.scans.flush()
        self.neo_driver.scans.flush()

    def get_by_id(self, identifier):
        return self.mongo_driver.scans.get_by_id(identifier)

    def delete_by_id(self, identifier):
        self.mongo_driver.scans.delete_by_id(identifier)
        self.neo_driver.scans.delete_by_id(identifier)


class Facts:
    def __init__(self, mongo_driver):
        self.mongo_driver = mongo_driver

    def get(self):
        return self.mongo_driver.facts.get()

    def get_by_id(self, identifier):
        return self.mongo_driver.facts.get_by_id(identifier)

    def get_by_name(self, name):
        return self.mongo_driver.facts.get_by_name(name)

    def update_by_id(self, identifier, data):
        return self.mongo_driver.facts.update_by_id(identifier, data)

    def flush(self):
        return self.mongo_driver.facts.flush()


class Algorithms:
    def __init__(self, neo_driver):
        self.neo_driver = neo_driver

    def page_rank(self):
        return self.neo_driver.algorithms.page_rank()

    def lpa(self):
        return self.neo_driver.algorithms.lpa()


class DataWriter(Singleton):
    def __init__(self):
        mongo_driver = MongoDriver()
        neo_driver = NeoDriver()

        self.facts = Facts(mongo_driver)
        self.scans = Scans(mongo_driver, neo_driver)
        self.results = Results(mongo_driver, neo_driver)
        self.collectors = Collectors(mongo_driver)
        self.collector_results = CollectorResults(mongo_driver)
        self.algorithms = Algorithms(neo_driver)
