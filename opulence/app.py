import opulence.collectors.app
import opulence.engine.app  # noqa: W0611
from opulence import App


@App.task(name="ping")
def ping():
    return "pong"
