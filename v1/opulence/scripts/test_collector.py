import sys

from dynaconf import settings

from opulence.common.job import Result
from opulence.common.plugins import PluginManager
import opulence.facts as facts

COLLECTORS_PATHS = settings.COLLECTORS_MODULES


def _random_input(input):
    random_input = {}
    for i in input().get_fields():
        random_input.update({i: f"test-{i}"})
    return input(**random_input)


def _gen_input(input_type):  # noqa: C901
    if input_type == facts.Domain:
        return facts.Domain(fqdn="wavely.fr")
    elif input_type == facts.IPv4:
        return facts.IPv4(address="31.3.142.135")
    elif input_type == facts.URI:
        return facts.URI(full_uri="http://wavely.fr")
    elif input_type == facts.Person:
        return facts.Person(firstname="John", lastname="Snow")
    elif input_type == facts.Phone:
        return facts.Phone(number="1-855-684-5463")
    elif input_type == facts.Username:
        return facts.Username(name="jurelou")
    elif input_type == facts.Email:
        return facts.Email(address="test@gmail.com")
    elif input_type == facts.GitRepository:
        return facts.GitRepository(url="https://github.com/cyberspacekittens/dnscat2")
    elif input_type == facts.Organization:
        return facts.Organization(name="wavely")
    elif input_type == facts.Flight:
        return facts.Flight(flight_number="EY17")
    else:
        return _random_input(input_type)


def _exec_collector(collector):
    print_state(collector)
    allowed_input = collector.get_allowed_input_as_list()
    test_inputs = []
    for input in allowed_input:
        test_inputs.append(_gen_input(input))

    for input in test_inputs:
        print("\n+ Running collector with input: ", input)
        print("+\t -> ", input.get_fields())
        result = Result(input=input)
        result = collector.run(result)

        print("@ Got result: ", result.status)
        if result.output:
            for i in result.output:
                print("@-----------------\n@\t->", i)
                if i:
                    for f in i.get_fields():
                        print("@\t\t->", f, ":", getattr(i, f).value)


def print_state(cls):
    print("----------------------------------------------")
    if not cls.errored:
        print(f"* Name: {cls.plugin_name}")
        print(f"* Description: {cls.plugin_description}")
        print(f"* Version: {cls.plugin_version}")
        print(f"* Category: {cls.plugin_category}")
        print("\t-----------")

    print(f"\n* STATUS: {cls.status}", " **")
    print(f"* INPUT: {cls.allowed_input}", " **")
    print("----------------------------------------------")


def main():
    if len(sys.argv) <= 1:
        print("Give me a collector name to execute!\n")
        print("Collectors loaded:")
        for path in COLLECTORS_PATHS:
            PluginManager().discover(path)
            for plugin in PluginManager().get_plugins(path):
                print(f"\t{plugin.plugin_name}")
        return
    for path in COLLECTORS_PATHS:
        PluginManager().discover(path)
        for plugin in PluginManager().get_plugins(path):
            if plugin.plugin_name == sys.argv[1]:
                _exec_collector(plugin)
                return f"DONE executing {plugin.plugin_name}"
            else:
                print(f" - skipped {plugin.plugin_name}")


if __name__ == "__main__":
    main()
