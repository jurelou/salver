from loguru import logger

from opulence.config import engine_config
from opulence.engine.app import celery_app

available_agents = {}


def refresh_agents():
    global available_agents

    def _get_agents():
        workers = celery_app.control.inspect().active_queues() or {}
        for name in workers.keys():
            conf = celery_app.control.inspect([name]).conf()[name]
            if "collectors" in conf:
                yield name, conf["collectors"]

    available_agents = {agent: config for agent, config in _get_agents()}
    logger.info(f"Available agents: {available_agents.keys()}")
