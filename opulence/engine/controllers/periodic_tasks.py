# -*- coding: utf-8 -*-
# import celery
from loguru import logger
from redbeat import RedBeatSchedulerEntry
from redbeat.schedulers import get_redis

def flush():
    logger.info("Flush periodic tasks")
    redis = get_redis()
    for key in redis.scan_iter("redbeat:*"):
        if key not in ("redbeat::lock"):
            redis.delete(key)


def add_periodic_task(app,  task_path, interval):
    print(f"Create periodic task {task_path} with {interval}")
    entry = RedBeatSchedulerEntry(f"pt_{task_path}", task_path, interval, app=app)
    entry.save()
