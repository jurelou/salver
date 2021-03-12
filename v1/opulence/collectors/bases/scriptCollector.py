import re
from subprocess import PIPE
from subprocess import Popen

from opulence.common.plugins.exceptions import PluginFormatError
from opulence.common.plugins.exceptions import PluginRuntimeError
from opulence.common.utils import is_list

from .baseCollector import BaseCollector


class ScriptCollector(BaseCollector):
    _script_path_ = ""
    _script_arguments_ = []

    def __init__(self, *args, **kwargs):
        if not self._script_path_:
            raise PluginFormatError("Incorrect script_path")
        super().__init__()

    @property
    def plugin_category(self):
        return ScriptCollector.__name__

    @property
    def script_path(self):
        return self._script_path_

    @property
    def script_arguments(self):
        return self._script_arguments_

    def launch(self, fact):
        if not self._script_arguments_:
            raise PluginFormatError("Incorrect script_arguments")

        if not is_list(fact):
            fact = [fact]
        args = self._find_and_replace_sigil(fact)
        stdout = self._exec(self.script_path, *args)
        return self.parse_result(stdout)

    def parse_result(self, result):
        raise NotImplementedError(
            "Method parse_result() should be defined for Plugin \
            <{}>".format(
                type(self).__name__,
            ),
        )

    @staticmethod
    def _exec(*cmd, stdin=None, ignore_error=False):
        def return_stdout(process_pipe):
            stdout, stderr = (x.strip().decode() for x in process_pipe.communicate())
            if not ignore_error and process_pipe.returncode:
                raise PluginRuntimeError(stderr)
            return stdout

        print(f"ScriptCollector: launch command {cmd}")
        if stdin is not None:
            out = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            out.stdin.write(str.encode(stdin))
        else:
            out = Popen(cmd, stdout=PIPE, stderr=PIPE)
        return return_stdout(out)

    @staticmethod
    def _replace_sigil(arg, facts):
        def find_sigil(arg):
            result = re.search("\\$(.*)\\$", arg)
            if result is not None:
                return result.group(1)
            return result

        found = find_sigil(arg)
        if found is None:
            return arg
        value = found
        try:
            (class_name, attribute_name) = value.split(".")
        except ValueError:
            return None
        for fact in facts:
            if str(type(fact).__name__) == class_name and hasattr(fact, attribute_name):
                replaced_value = getattr(fact, attribute_name).value
                value_to_replace = f"${value}$"
                return arg.replace(value_to_replace, replaced_value)
        return None

    def _find_and_replace_sigil(self, facts):
        args = self.script_arguments
        res = []

        if not is_list(args):
            args = [args]
        for arg in args:
            replaced = self._replace_sigil(arg, facts)
            if replaced is not None:
                res.append(replaced)
        return res
