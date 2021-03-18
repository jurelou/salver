# -*- coding: utf-8 -*-
import unittest

from opulence.common.fields import BaseField
from opulence.common.fields import IntegerField
from opulence.common.fields import StringField
from opulence.facts.bases import BaseFact


class Person(BaseFact):
    _name_ = "superplugin"
    _description_ = "desc"
    _author_ = "nobody"
    _version_ = 42

    def setup(self):
        self.a = StringField(mandatory=True)
        self.b = IntegerField()


class TestFactSerialisation(unittest.TestCase):
    def test_serialisation_01(self):
        p = Person(a="a", b=2)
        p2 = Person(a="a", b=2)
        new_p = Person.from_json(p.to_json())
        new_p2 = Person.from_json(p2.to_json())
        self.assertEqual(p, new_p)
        self.assertEqual(new_p, new_p2)
        for (a, b), (c, d) in zip(p.get_fields().items(), new_p.get_fields().items()):
            self.assertTrue(a == c)
            self.assertTrue(b == d)
        self.assertEqual(new_p.to_json(), p.to_json())


class TestFact(unittest.TestCase):
    def test_simple_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField()

        fact = Person()
        self.assertEqual(fact.plugin_name, "superplugin")
        self.assertEqual(fact.plugin_description, "desc")
        self.assertEqual(fact.plugin_author, "nobody")
        self.assertEqual(fact.plugin_version, 42)
        self.assertFalse(fact.errored)
        self.assertEqual(fact.plugin_dependencies, ())

        self.assertTrue(fact.is_valid())
        self.assertIsInstance(fact.a, StringField, BaseField)
        self.assertIsNone(fact.a.value)
        self.assertIsNone(fact.a.default)
        self.assertFalse(fact.a.mandatory)

    def test_valid_fact_0(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True)
                self.b = StringField()

        fact = Person(a="yes")
        self.assertTrue(fact.is_valid())

    def test_valid_fact_1(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True, default="aze")
                self.b = StringField()

        fact = Person(a="yes")
        self.assertTrue(fact.is_valid())

    def test_invalid_fact_0(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True, default="def")
                self.b = StringField()

        fact = Person()
        self.assertFalse(fact.is_valid())

    def test_invalid_fact__1(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True, default="def")
                self.b = StringField()

        fact = Person(a="def")
        self.assertFalse(fact.is_valid())

    def test_complex_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(value="Joe", mandatory=True)
                self.b = StringField(default="James")
                self.c = IntegerField(mandatory=True)
                self.d = IntegerField()
                self.x = "x"

        fact = Person()
        self.assertEqual(fact.plugin_name, "superplugin")
        self.assertEqual(fact.plugin_description, "desc")
        self.assertEqual(fact.plugin_author, "nobody")
        self.assertEqual(fact.plugin_version, 42)
        self.assertFalse(fact.errored)
        self.assertEqual(fact.plugin_dependencies, ())

        self.assertFalse(fact.is_valid())

        self.assertIsInstance(fact.a, StringField, BaseField)
        self.assertEqual(fact.a.value, "Joe")
        self.assertIsNone(fact.a.default)
        self.assertTrue(fact.a.mandatory)

    def test_missing_author_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _version_ = 42

            def setup(self):
                self.a = StringField(value="Joe", mandatory=True)

        fact = Person()

        self.assertTrue(fact.errored)
        self.assertTrue(fact.is_valid())

    def test_missing_description_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _author_ = "nobody"

        fact = Person()

        self.assertTrue(fact.errored)
        self.assertTrue(fact.is_valid())

    def test_facts_hash(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _author_ = "nobody"
            _description_ = "desc"

            def setup(self):
                self.a = StringField()

        a = Person()
        b = Person()
        c = Person()
        self.assertEqual(hash(a), hash(b), hash(c))

    def test_facts_hash_invalid_plugin(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField()

        a = Person()
        b = Person()
        c = Person()
        self.assertEqual(hash(a), hash(b), hash(c))

    def test_empty_facts_hash_comparison(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

        a = Person()
        aa = Person()
        b = Person(a="joe")
        c = Person(a="joe")

        self.assertNotEqual(hash(a), hash(b))
        self.assertEqual(hash(a), hash(aa))
        self.assertEqual(hash(b), hash(c))

        self.assertEqual(a.plugin_category, "fact")

    def test_facts_hash_comparison(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField()

        a = Person(a="joe")
        b = Person(a="joe")
        c = Person(a="job")
        self.assertEqual(hash(a), hash(b))

        self.assertNotEqual(hash(a), hash(c))
        self.assertNotEqual(hash(b), hash(c))

    def test_complex_facts_hash_comparison(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField(default="42")
                self.b = IntegerField(default=42)
                self.c = IntegerField(default=424242)

        a = Person(a="42", b=42, c=424242)
        b = Person(a=42, b="42")
        c = Person(a="42", b=42, c=424242)
        d = Person()
        e = Person(a="42", b=43, c=424242)
        self.assertEqual(hash(a), hash(b), hash(c))
        self.assertEqual(hash(b), hash(c), hash(d))
        self.assertNotEqual(hash(e), hash(a))
        self.assertNotEqual(hash(e), hash(b))
        self.assertNotEqual(hash(e), hash(c))
        self.assertNotEqual(hash(e), hash(d))

    def test_get_info(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField(default="42")
                self.b = IntegerField()
                self.c = IntegerField(default=424242)

        a = Person(a="42", c=424242)

        infos = a.get_info()
        self.assertTrue("plugin_data" in infos)

        should_be = {
            "a": {"value": "42", "default": "42", "mandatory": False},
            "b": {"value": None, "default": None, "mandatory": False},
            "c": {"value": 424242, "default": 424242, "mandatory": False},
        }
        self.assertEqual(should_be, infos["fields"])

    def test_fact_additional_fields_equal(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField()

        factA = Person(a="Hello", additional="world")
        factB = Person(a="Hello", additional="world")

        self.assertTrue(factA.is_valid())
        self.assertEqual(factA, factB)
        self.assertEqual(hash(factA), hash(factB))

    def test_fact_additional_fields_not_equal(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField()

        factA = Person(a="Hello", additional="world")
        factB = Person(a="Hello", additional="hello")

        self.assertTrue(factA.is_valid())
        self.assertNotEqual(factA, factB)
        self.assertNotEqual(hash(factA), hash(factB))

    def test_fact_additional_fields_not_equal_2(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField()

        factA = Person(a="Hello", additional="world")
        factB = Person(a="Hello", hello="world")

        self.assertTrue(factA.is_valid())
        self.assertTrue(factB.is_valid())

        self.assertNotEqual(factA, factB)
        self.assertNotEqual(hash(factA), hash(factB))

    def test_fact_compare_to_dummy(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField()

        fact = Person(a="Hello", additional="world")

        self.assertFalse(fact == 42)
