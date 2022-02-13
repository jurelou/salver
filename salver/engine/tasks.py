from salver.engine import celery_app
from salver.engine.controllers import agent_tasks


@celery_app.task
def toto():
    print("TOTO Task")
