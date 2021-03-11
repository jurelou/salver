class BaseOpulenceException(Exception):
    pass


class TaskTimeoutError(BaseOpulenceException):
    def __init__(self, value=None):
        self.value = value or ""

    def __str__(self):
        return f"Celery task timeout: ({self.value})"


class CollectorNotFound(BaseOpulenceException):
    def __init__(self, collector_name):
        self.collector_name = collector_name

    def __str__(self):
        return f"Collector {self.collector_name} not found"
