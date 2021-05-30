# -*- coding: utf-8 -*-
from salver.common.exceptions import SalverException

<<<<<<< HEAD

=======
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
class CollectorNotFound(SalverException):
    def __init__(self, collector_name):
        self.collector_name = collector_name

    def __str__(self):
<<<<<<< HEAD
        return f'Collector {self.collector_name} not found.'
=======
        return f'Collector {self.collector_name} not found.'
>>>>>>> 500275e8119b1fe94ff9b5b505d52a5ad88a8e96
