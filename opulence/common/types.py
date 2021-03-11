import inspect

from opulence.common.fact import BaseFact


def collect_fact_types(types):
    ftypes = []
    if not isinstance(types, list):
        types = [types]
    for t in types:
        if t not in ftypes and inspect.isclass(t) and issubclass(t, BaseFact):
            ftypes.append(t)
    return ftypes


class BaseSet:
    def __init__(self, *args):
        self.params = collect_fact_types(list(args))

    def check_against(self, target) -> bool:  # pragma: no cover
        raise NotImplementedError(
            f"Set {type(self).__name__} does not contains a `check_against` method.",
        )

    def select_from(self, props):  # pragma: no cover
        raise NotImplementedError(
            f"Set {type(self).__name__} does not contains a `select_from` method.",
        )

    def json(self):
        return {
            "type": type(self).__name__,
            "params": [p.__name__ for p in self.params],
        }


class Union(BaseSet):
    def check_against(self, target) -> bool:
        target = collect_fact_types(target)
        for t in target:
            if t in self.params:
                return True
        return False

    def select_from(self, props):
        for prop in props:
            if type(prop) in self.params:
                return prop
        return None


class Group(BaseSet):
    def check_against(self, target) -> bool:
        target = collect_fact_types(target)
        return set(target) == set(self.params)

    def select_from(self, props):
        res = []
        for prop in props:
            if type(prop) in self.params:
                res.append(prop)
        return res or None


# class   Unique(BaseSet):
#     def check_against(self, target) -> bool:
#         # TODO

#     def select_from(self, props):
#         # TODO

# class   Multiple(BaseSet):
#     def check_against(self, target) -> bool:
#         # TODO

#     def select_from(self, props):
#         # TODO
