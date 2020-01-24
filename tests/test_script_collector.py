import unittest

from opulence.collectors.bases import ScriptCollector
from opulence.common.plugins import exceptions
from opulence.facts import Person


class testCollector(ScriptCollector):
    _name_ = "test"
    _description_ = "testdesc"
    _author_ = "test"
    _version_ = 1
    _allowed_input_ = Person

    _script_path_ = "test"
    _script_arguments_ = ["notreplaced", "$Person.firstname$", "notreplaced"]


class TestScriptCollector(unittest.TestCase):
    def test_script_path_empty(self):
        class testCollector(ScriptCollector):
            _name_ = "test"
            _description_ = "testdesc"
            _author_ = "test"
            _version_ = 1
            _allowed_input_ = Person

            _script_arguments_ = ["notreplaced", "$Person.firstname$", "notreplaced"]

        with self.assertRaises(exceptions.PluginFormatError):
            testCollector()

    def test_script_replace(self):
        collector = testCollector()
        a = Person(firstname="fa", lastname="la")
        sigiled = collector._find_and_replace_sigil([a])
        self.assertEqual(sigiled, ["notreplaced", "fa", "notreplaced"])

    def test_script_replace_none(self):
        collector = testCollector()
        sigiled = collector._find_and_replace_sigil(["nope"])
        self.assertEqual(sigiled, ["notreplaced", "notreplaced"])

    def test_script_script_args_as_array(self):
        collector = testCollector()
        collector._script_arguments_ = "$Person.lastname$"
        a = Person(firstname="fa", lastname="la")
        sigiled = collector._find_and_replace_sigil([a])
        self.assertEqual(sigiled, ["la"])

    def test_script_script_args_not_splitable(self):
        collector = testCollector()
        collector._script_arguments_ = "$thereisnodot$"
        a = Person(firstname="fa", lastname="la")
        sigiled = collector._find_and_replace_sigil([a])
        self.assertEqual(sigiled, [])


if __name__ == "__main__":
    unittest.main()
