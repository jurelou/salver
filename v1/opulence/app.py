from opulence import App
import opulence.collectors.app
import opulence.engine.app  # noqa: W0611


@App.task(name="ping")
def ping():
    return "pong"
