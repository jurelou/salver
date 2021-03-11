class TaskError(Exception):
    def __init__(self, value=None):
        self.value = value or ""


class TaskTimeoutError(TaskError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Task timeout: ({})".format(self.value)
