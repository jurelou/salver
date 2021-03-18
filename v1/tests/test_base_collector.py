# -*- coding: utf-8 -*-
import unittest

from opulence.collectors.bases import BaseCollector
from opulence.common.job import StatusCode
from opulence.common.patterns import Composite
from opulence.common.plugins import exceptions
from opulence.facts import Person


class TestBaseCollector(unittest.TestCase):
    def test_no_allowed_input(self):
        class Dummy(BaseCollector):
            _name_ = "dummy collector"
            _description_ = "This is an example collector"
            _author_ = "Louis"
            _version_ = 1
            _allowed_input_ = []

            def launch(self, fact):
                return "done"

        with self.assertRaises(exceptions.PluginFormatError) as exc:
            Dummy()

    def test_no_launch(self):
        class Dummy(BaseCollector):
            _name_ = "dummy collector"
            _description_ = "This is an example collector"
            _author_ = "Louis"
            _version_ = 1
            _allowed_input_ = Person

        d = Dummy()
        with self.assertRaises(NotImplementedError) as exc:
            d.launch(Person())

    # def test_run_empty(self):
    #     class Dummy(BaseCollector):
    #         _name_ = "dummy collector"
    #         _description_ = "This is an example collector"
    #         _author_ = "Louis"
    #         _version_ = 1
    #         _allowed_input_ = Person

    #     d = Dummy()
    #     res = d.run("nope")
    #     self.assertEqual(res.status["status"], StatusCode.empty)

    # def test_run_invalid(self):
    #     class Dummy(BaseCollector):
    #         _name_ = "dummy collector"
    #         _description_ = "This is an example collector"
    #         _author_ = "Louis"
    #         _version_ = 1
    #         _allowed_input_ = Person

    #         def launch(self, fact):
    #             return "done"

    #     d = Dummy()
    #     res = d.run(Person())
    #     self.assertEqual(res.status["status"], StatusCode.invalid_input)

    # def test_run_collector_throw(self):
    #     class Dummy(BaseCollector):
    #         _name_ = "dummy collector"
    #         _description_ = "This is an example collector"
    #         _author_ = "Louis"
    #         _version_ = 1
    #         _allowed_input_ = Person

    #         def launch(self, fact):
    #             raise NotImplementedError("yeah")

    #     d = Dummy()
    #     res = d.run(Person(firstname="john", lastname="snow"))
    #     self.assertEqual(res.status["status"], StatusCode.error)
    #     self.assertEqual(res.status["error"], "yeah")

    # def test_run_collector_with_composite(self):
    #     class Dummy(BaseCollector):
    #         _name_ = "dummy collector"
    #         _description_ = "This is an example collector"
    #         _author_ = "Louis"
    #         _version_ = 1
    #         _allowed_input_ = Composite(Person, Person)

    #         def launch(self, fact):
    #             print("ok")

    #     d = Dummy()
    #     john = Person(firstname="john", lastname="snow")
    #     snow = Person(firstname="snow", lastname="john")
    #     res = d.run(Composite(john, snow))
    #     self.assertEqual(res.status["status"], StatusCode.finished)
    #     self.assertEqual(res.status["error"], None)

    #     infos = d.get_info()
    #     self.assertTrue("plugin_data" in infos)
    #     self.assertTrue("allowed_input" in infos)
