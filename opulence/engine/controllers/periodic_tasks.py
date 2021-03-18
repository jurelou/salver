# -*- coding: utf-8 -*-
# import celery
from loguru import logger
from redbeat import RedBeatSchedulerEntry
from redbeat.schedulers import get_redis

# from opulence.config import engine_config

# def configure_tasks():
#     interval = celery.schedules.schedule(run_every=engine_config.refresh_agents_interval)
#     entry = RedBeatSchedulerEntry("reload_agents", 'opulence.engine.tasks.reload_agents', interval, app=celery_app)
#     entry.save()


def flush():
    logger.info("Flush periodic tasks")
    redis = get_redis()
    for key in redis.scan_iter("redbeat:*"):
        if key not in ("redbeat::lock"):
            redis.delete(key)


def add_periodic_task(app, interval, task_path):
    print(f"Create periodic task {task_path} with {interval}")
    entry = RedBeatSchedulerEntry(f"pt_{task_path}", task_path, interval, app=app)
    entry.save()
