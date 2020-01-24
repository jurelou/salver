from opulence import App


def load():
    return App.signature("collectors:reload_collectors", immutable=True)


def list():
    return App.signature("collectors:list_collectors", immutable=True)


def info():
    pass


def launch(collector_name, input_fact):
    return App.signature(
        "collectors:execute_collector_by_name",
        args=[collector_name, input_fact],
        immutable=True,
    )
