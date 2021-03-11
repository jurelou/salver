import json
import unittest

from opulence.common.fields import IntegerField, StringField
from opulence.common.job import Composable, Result
from opulence.common.jsonEncoder import (
    custom_dumps, custom_loads, decode, encode
)
from opulence.common.patterns import Composite
from opulence.common.plugins import BasePlugin, PluginStatus
from opulence.facts.bases import BaseFact


class FactA(BaseFact):
    _name_ = "x"
    _description_ = "xx"
    _author_ = "xxx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField(mandatory=False)
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class FactB(BaseFact):
    _name_ = "x"
    _description_ = "xx"
    _author_ = "xxx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField(mandatory=False)
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class TestJsonEncodeJob(unittest.TestCase):
    def test_encode_simple_json(self):
        valid_json = {"john": 42, "42": "john"}

        to_json = custom_dumps(valid_json)
        from_json = custom_loads(to_json)

        self.assertEqual(valid_json, from_json)

    def test_encode_PluginStatus(self):
        e = PluginStatus.ERROR
        e_json = json.dumps(e, cls=encode)
        new_e = json.loads(e_json, object_hook=decode)
        self.assertEqual(e, new_e)
        self.assertEqual(new_e, PluginStatus.ERROR)

    def test_encode_simple_job(self):
        r = Result(input=FactA(), output=FactB())
        r_json = r.to_json()
        new_r = Result.from_json(r_json)
        self.assertEqual(r.identifier, new_r.identifier)
        self.assertEqual(r.input.get(), new_r.input.get())
        self.assertEqual(r.output, new_r.output)
        for a, b in zip(r.output, new_r.output):
            self.assertEqual(a, b)
        self.assertEqual(r.clock.start_date, new_r.clock.start_date)
        self.assertEqual(r.clock.end_date, new_r.clock.end_date)

    def test_encode_complex_job_01(self):
        r = Result()
        r.input = FactA(a="42", b=2)
        r.output = FactB(a="42", b=2)
        r_json = r.to_json()
        new_r = Result.from_json(r_json)

        self.assertEqual(r.identifier, new_r.identifier)

        self.assertIsInstance(r.input, Composable)
        self.assertIsInstance(new_r.input, Composable)
        self.assertEqual(r.input.get(), new_r.input.get())
        self.assertEqual(r.output, new_r.output)

    def test_encode_complex_job_02(self):
        r = Result()
        r.input = Composite(FactA(a="42", b=2), FactB(a=1, b=2))
        r.output = [FactA(a=1, b=4), FactA(a=2, b=3), FactB(a=3, b=2), FactB(a=4, b=1)]
        r_json = r.to_json()
        new_r = Result.from_json(r_json)

        self.assertEqual(r.identifier, new_r.identifier)

        self.assertIsInstance(r.input, Composable)
        self.assertIsInstance(new_r.input, Composable)
        self.assertEqual(r.input.get(), new_r.input.get())

        self.assertEqual(r.output, new_r.output)
        self.assertEqual(len(r.output), 4)

    def test_encode_job_using_json(self):
        r = Result()
        r.input = FactA(a="42", b=2)
        r.output = FactB(a="42", b=2)
        r.clock.start()
        r_json = json.dumps(r, cls=encode)
        new_r = json.loads(r_json, object_hook=decode)
        self.assertEqual(r.identifier, new_r.identifier)
        self.assertEqual(r.input.get(), new_r.input.get())
        self.assertEqual(r.output, new_r.output)
        for a, b in zip(r.output, new_r.output):
            self.assertEqual(a, b)
        self.assertEqual(r.clock.start_date, new_r.clock.start_date)
        self.assertEqual(r.clock.end_date, new_r.clock.end_date)


class TestJsonEncodeStringField(unittest.TestCase):
    def test_encode_stringfield(self):
        s = StringField(value="Foo", default="Bar", mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, str)
        self.assertIsInstance(new_s.default, str)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)

    def test_encode_cast_stringfield(self):
        s = StringField(value=32, default=42, mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, str)
        self.assertIsInstance(new_s.default, str)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)


class TestJsonEncodeIntegerField(unittest.TestCase):
    def test_encode_integerfield(self):
        s = IntegerField(value=24, default=42, mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, int)
        self.assertIsInstance(new_s.default, int)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)

    def test_encode_cast_integerield(self):
        s = IntegerField(value="42", default="24", mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, int)
        self.assertIsInstance(new_s.default, int)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)


if __name__ == "__main__":
    unittest.main()
