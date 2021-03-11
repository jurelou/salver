from .patterns import JsonSerializable
from .utils import datetime_to_str, now, str_to_datetime


class Clock(JsonSerializable):
    def __init__(self, start_date=None, end_date=None, started=False):
        self.start_date = start_date
        self.end_date = end_date
        self.started = started

    def start(self):
        self.started = True
        self.end_date = None
        self.start_date = now()

    def stop(self):
        self.started = False
        self.end_date = now()

    @property
    def time_elapsed(self):
        assert self.start_date, "Can't check 'time_elapsed' on an unstarted Clock"
        if self.end_date:
            return self.end_date - self.start_date
        return now() - self.start_date

    def to_json(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            "started": self.started,
            "start_date": datetime_to_str(self.start_date),
            "end_date": datetime_to_str(self.end_date),
        }
        return obj_dict

    @staticmethod
    def from_json(json_dict):
        json_dict.update(
            {
                "start_date": str_to_datetime(json_dict["start_date"]),
                "end_date": str_to_datetime(json_dict["end_date"]),
            }
        )
        return super(Clock, Clock).from_json(json_dict)
