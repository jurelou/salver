import json
import unittest

from opulence.common.fields import IntegerField, StringField
from opulence.common.job import Composable, Result, StatusCode
from opulence.common.jsonEncoder import decode, encode
from opulence.common.patterns import Composite
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


class TestComposables(unittest.TestCase):
    def test_composable_eq(self):
        a = FactA(a=1)
        b = FactA(a=2)
        c = Composable(Composite(a, b))

        a1 = FactA(a=1)
        b1 = FactA(a=2)
        c1 = Composable(Composite(a1, b1))

        self.assertTrue(c == c1)

    def test_composable_eq_2(self):
        a = FactA(a=1)
        c = Composable(Composite(a))

        a1 = FactA(a=1)
        c1 = Composable(a1)

        self.assertTrue(c == c1)

    def test_composable_not_eq(self):
        a = FactA(a=1)
        b = FactA(a=2)
        c = Composable(Composite(a, b))

        a1 = FactA(a=1)

        self.assertTrue(c != a1)

    def test_composable_not_eq_2(self):
        a = FactA(a=1)
        b = FactA(a=2)
        c = Composable(Composite(a, b))

        a1 = FactA(a=1)
        b1 = FactA(a=4242)
        c1 = Composable(Composite(a1, b1))

        self.assertTrue(c != c1)


class TestJobResult(unittest.TestCase):
    def test_job_result_composite(self):
        a = FactA()
        b = FactA()
        j = Result(input=Composite(a, b))

        j.status = StatusCode.finished
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(
            False,
            StatusCode.is_errored(new_j.status["status"]),
            StatusCode.is_errored(j.status["status"]),
        )
        self.assertEqual(j.status, new_j.status)
        self.assertEqual("Finished", j.status["code"], new_j.status["code"])
        self.assertEqual(j.input, new_j.input)

    def test_job_result_error_msg(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.finished, "this is an error"
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(
            False,
            StatusCode.is_errored(new_j.status["status"]),
            StatusCode.is_errored(j.status["status"]),
        )
        self.assertEqual(j.status, new_j.status)
        self.assertEqual("Finished", j.status["code"], new_j.status["code"])
        self.assertEqual("this is an error", j.status["error"], new_j.status["error"])

    def test_job_result_errored(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.error
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(
            True,
            StatusCode.is_errored(new_j.status["status"]),
            StatusCode.is_errored(j.status["status"]),
        )
        self.assertEqual(j.status, new_j.status)

    def test_job_result_errored_bis(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.rate_limited
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(
            True,
            StatusCode.is_errored(new_j.status["status"]),
            StatusCode.is_errored(j.status["status"]),
        )
        self.assertEqual(j.status, new_j.status)
        self.assertEqual(j.output, None)

    def test_job_result_output(self):
        a = FactA()
        b = FactA(a=1, b=2, c=3)
        j = Result(input=a, output=b)

        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)
        self.assertEqual(new_j.output, j.output)
        self.assertEqual(False, StatusCode.is_errored(j.status["status"]))
        self.assertEqual(1, len(j.output))
        self.assertEqual(j.output[0], b)
        self.assertEqual(j.output[0].get_info(), b.get_info())

    def test_job_result_output2(self):
        r = Result()
        r.input = FactA(a=1, b=2)
        r.output = [FactA(a=10, b=20), FactA(a=12, b=22)]

        r_json = r.to_json()
        r_json2 = json.dumps(r, cls=encode)
        new_r = json.loads(r_json2, object_hook=decode)
        new_r_json = new_r.to_json()

        self.assertEqual(r_json["input"], new_r_json["input"])
        for a, b in zip(r_json["input"], new_r_json["input"]):
            self.assertTrue(a == b)

        self.assertEqual(r_json["output"], new_r_json["output"])
        for a, b in zip(r_json["output"], new_r_json["output"]):
            self.assertTrue(a == b)

    def test_job_result_output3(self):
        r = Result()
        r.input = Composite(FactA(a=1, b=2), FactA(a=10, b=20))
        r.output = FactA(a=10, b=20)

        r_json = r.to_json()
        output_should_be = [
            {
                "__class__": "FactA",
                "__module__": "test_job",
                "fields": {
                    "a": {
                        "__class__": "IntegerField",
                        "__module__": "opulence.common.fields.fields",
                        "value": 10,
                        "default": None,
                        "mandatory": False,
                    },
                    "b": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "20",
                        "default": "b",
                        "mandatory": False,
                    },
                    "c": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "c",
                        "default": "c",
                        "mandatory": False,
                    },
                },
            },
        ]

        input_should_be = [
            {
                "__class__": "FactA",
                "__module__": "test_job",
                "fields": {
                    "a": {
                        "__class__": "IntegerField",
                        "__module__": "opulence.common.fields.fields",
                        "value": 1,
                        "default": None,
                        "mandatory": False,
                    },
                    "b": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "2",
                        "default": "b",
                        "mandatory": False,
                    },
                    "c": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "c",
                        "default": "c",
                        "mandatory": False,
                    },
                },
            },
            {
                "__class__": "FactA",
                "__module__": "test_job",
                "fields": {
                    "a": {
                        "__class__": "IntegerField",
                        "__module__": "opulence.common.fields.fields",
                        "value": 10,
                        "default": None,
                        "mandatory": False,
                    },
                    "b": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "20",
                        "default": "b",
                        "mandatory": False,
                    },
                    "c": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "c",
                        "default": "c",
                        "mandatory": False,
                    },
                },
            },
        ]

        self.assertEqual(r_json["output"], output_should_be)
        self.assertEqual(r_json["input"], input_should_be)
        new_r = Result.from_json(r_json)
        new_r_json = new_r.to_json()

        for a, b in zip(r.to_json()["input"], new_r_json["input"]):
            self.assertTrue(a == b)
        for a, b in zip(r.to_json()["output"], new_r_json["output"]):
            self.assertTrue(a == b)

    def test_job_empty(self):
        r = Result()
        r_json = r.to_json()
        new_r = Result.from_json(r_json)
        self.assertEqual(new_r.to_json(), r.to_json())

    def test_job_not_altered(self):
        r = Result()
        r.input = Composite(FactA(a=1, b=2), FactA(a=10, b=20))
        r.output = FactA(a=30, b=40)
        r_json = r.to_json()

        input_should_be = [
            {
                "__class__": "FactA",
                "__module__": "test_job",
                "fields": {
                    "a": {
                        "__class__": "IntegerField",
                        "__module__": "opulence.common.fields.fields",
                        "value": 1,
                        "default": None,
                        "mandatory": False,
                    },
                    "b": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "2",
                        "default": "b",
                        "mandatory": False,
                    },
                    "c": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "c",
                        "default": "c",
                        "mandatory": False,
                    },
                },
            },
            {
                "__class__": "FactA",
                "__module__": "test_job",
                "fields": {
                    "a": {
                        "__class__": "IntegerField",
                        "__module__": "opulence.common.fields.fields",
                        "value": 10,
                        "default": None,
                        "mandatory": False,
                    },
                    "b": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "20",
                        "default": "b",
                        "mandatory": False,
                    },
                    "c": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "c",
                        "default": "c",
                        "mandatory": False,
                    },
                },
            },
        ]

        output_should_be = [
            {
                "__class__": "FactA",
                "__module__": "test_job",
                "fields": {
                    "a": {
                        "__class__": "IntegerField",
                        "__module__": "opulence.common.fields.fields",
                        "value": 30,
                        "default": None,
                        "mandatory": False,
                    },
                    "b": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "40",
                        "default": "b",
                        "mandatory": False,
                    },
                    "c": {
                        "__class__": "StringField",
                        "__module__": "opulence.common.fields.fields",
                        "value": "c",
                        "default": "c",
                        "mandatory": False,
                    },
                },
            },
        ]

        self.assertEqual(input_should_be, r_json["input"])
        self.assertEqual(output_should_be, r_json["output"])
