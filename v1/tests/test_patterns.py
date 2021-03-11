import unittest

from opulence.common.patterns import Composite, JsonSerializable, Singleton


class Foobar(JsonSerializable):
    a = 1
    b = "foo"
    c = {"bar": "baz", "foo": 42}


class TestJsonSerializable(unittest.TestCase):
    def test_json_serialization(self):
        foo = Foobar()
        foo_json = foo.to_json()
        foo_back = Foobar.from_json(foo_json)
        self.assertEqual(foo.a, foo_back.a)
        self.assertEqual(foo.b, foo_back.b)
        self.assertEqual(foo.c, foo_back.c)
        self.assertEqual(foo.__class__.__name__, foo_back.__class__.__name__)


class TestSingleton(unittest.TestCase):
    def test_simple_singleton(self):
        class toto(Singleton):
            pass

        a = toto()
        b = toto()
        self.assertEqual(id(a), id(b))

    def test_inheritance_singleton(self):
        class toto(Singleton):
            pass

        class tata(toto):
            pass

        a = toto()
        b = tata()
        self.assertNotEqual(id(a), id(b))


class TestComposite(unittest.TestCase):
    def test_simple_composite(self):
        c = Composite("a", "b", "c", "d", 42, {"quarente-deux": 42})
        expected = ["a", "b", "c", "d", 42, {"quarente-deux": 42}]
        self.assertEqual(c.elements, expected)

    def test_complex_composite(self):
        c = Composite((1), (42, "bb"), ({"One": 1}, "cc"), "d", 0.4242, ["one", 2, 3.0])
        expected = [1, 42, "bb", {"One": 1}, "cc", "d", 0.4242, "one", 2, 3.0]
        self.assertEqual(c.elements, expected)
