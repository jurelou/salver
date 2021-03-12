from opulence.common.job import StatusCode
from opulence.common.patterns import is_composite
from opulence.common.plugins import BasePlugin
from opulence.common.plugins.exceptions import PluginFormatError
from opulence.common.plugins.exceptions import RateLimitException
from opulence.common.tokenbucket.bucketsManager import Buckets
from opulence.common.utils import is_iterable
from opulence.common.utils import is_list
from opulence.facts.bases import BaseFact


class BaseCollector(BasePlugin):
    _allowed_input_ = ()
    _active_scanning_ = True
    _rate_limit_ = []

    def __init__(self, *args, **kwargs):
        if not self._allowed_input_:
            raise PluginFormatError(
                "<{}> needs at least one allowed_input".format(type(self).__name__),
            )
        super().__init__()

    @property
    def plugin_category(self):
        return BaseCollector.__name__

    @property
    def allowed_input(self):
        return (
            self._allowed_input_
            if is_list(self._allowed_input_)
            else [self._allowed_input_]
        )

    @staticmethod
    def _sanitize_input(input):
        if not input:
            return True, (StatusCode.empty, "No input provided")
        for i in input:
            if not i.is_valid():
                return (
                    True,
                    (
                        StatusCode.invalid_input,
                        "Invalid input provided: " + str(i.get_info()),
                    ),
                )
        return False, None

    @staticmethod
    def _sanitize_output(output):
        if is_iterable(output):
            output = list(output)
        if not is_list(output):
            output = [output]
        output = list(filter(None, output))
        print("Got: {} output facts".format(len(output)))
        return [out for out in output if isinstance(out, BaseFact) and out.is_valid()]

    def run(self, result):
        print("Running collector {}".format(type(self).__name__))
        Buckets.Get_Buckets(self._name_, self._rate_limit_)
        result.collector_data = self.get_info()
        ret, state = self._sanitize_input(result.input.get(force_array=True))
        result.status = StatusCode.ready

        if ret:
            result.status = state
            return result
        try:
            print(f"Clock starting for {self.plugin_name}")
            if Buckets.reduce(self._name_) is False:
                refill_time = str(Buckets.nextRefill(self._name_))
                raise RateLimitException(
                    f"API: out of tokens, refill in {refill_time}",
                )
            result.clock.start()
            result.status = StatusCode.started
            output = self.launch(result.input.get())
            result.clock.stop()
            print(f"Stopped clock for {self.plugin_name}")
            result.output = self._sanitize_output(output)
            result.status = StatusCode.finished
        except RateLimitException as err:
            result.clock.stop()
            result.status = 300, str(err)
            raise
        except Exception as err:
            print(f"Error in run() from ({self.plugin_name}): {err}")
            result.clock.stop()
            result.status = StatusCode.error, str(err)
        finally:
            return result

    def launch(self, fact):
        raise NotImplementedError(
            "Method launch() should be defined for Plugin \
            <{}>".format(
                type(self).__name__,
            ),
        )

    def get_allowed_input_as_list(self, full_data=False):
        ret = []
        for input in self.allowed_input:
            if is_composite(input):
                if full_data:
                    ret.append([i().get_info() for i in input.elements])
                else:
                    ret.append([i for i in input.elements])
            else:
                if full_data:
                    ret.append(input().get_info())
                else:
                    ret.append(input)
        return ret

    def get_info(self):

        data = {
            "active_scanning": self._active_scanning_,
            "allowed_input": self.get_allowed_input_as_list(full_data=True),
            "api_rate": self._api_rate_,
        }
        return {**super().get_info(), **data}
