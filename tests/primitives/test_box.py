import unittest

from dspy.primitives.box import Box


class TestBox(unittest.TestCase):

    def setUp(self):
        self.box = Box("test", source=True)

    def test_init(self):
        self.assertEqual(self.box._value, "test")
        self.assertEqual(self.box._source, True)

    def test_repr(self):
        self.assertEqual(repr(self.box), "test")

    def test_str(self):
        self.assertEqual(str(self.box), "test")

    def test_bool(self):
        self.assertEqual(bool(self.box), True)

    def test_getattr(self):
        self.assertEqual(self.box.__getattr__("upper")(), "TEST")
        with self.assertRaises(AttributeError):
            self.box.__getattr__("non_existent")

if __name__ == "__main__":
    unittest.main()
