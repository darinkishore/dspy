import unittest

from dspy.primitives import Example


class TestExample(unittest.TestCase):
    def setUp(self):
        self.example = Example(base={"key1": "value1", "key2": "value2"}, key3="value3")

    def test_init(self):
        self.assertEqual(self.example._store, {"key1": "value1", "key2": "value2", "key3": "value3"})
        self.assertEqual(self.example._demos, [])
        self.assertIsNone(self.example._input_keys)

    def test_getattr(self):
        self.assertEqual(self.example.key1, "value1")
        with self.assertRaises(AttributeError):
            self.example.non_existent

    def test_setattr(self):
        self.example.key4 = "value4"
        self.assertEqual(self.example.key4, "value4")

    def test_getitem(self):
        self.assertEqual(self.example["key1"], "value1")

    def test_setitem(self):
        self.example["key4"] = "value4"
        self.assertEqual(self.example["key4"], "value4")

    def test_delitem(self):
        del self.example["key1"]
        with self.assertRaises(KeyError):
            self.example["key1"]

    def test_contains(self):
        self.assertTrue("key2" in self.example)
        self.assertFalse("non_existent" in self.example)

    def test_len(self):
        self.assertEqual(len(self.example), 3)

    def test_repr(self):
        self.assertEqual(repr(self.example), "Example({'key2': 'value2', 'key3': 'value3', 'key4': 'value4'}) (input_keys=None)")

    def test_str(self):
        self.assertEqual(str(self.example), "Example({'key2': 'value2', 'key3': 'value3', 'key4': 'value4'}) (input_keys=None)")

    def test_eq(self):
        other = Example(base={"key2": "value2", "key3": "value3", "key4": "value4"})
        self.assertTrue(self.example == other)

    def test_hash(self):
        self.assertEqual(hash(self.example), hash(Example(base={"key2": "value2", "key3": "value3", "key4": "value4"})))

    def test_keys(self):
        self.assertEqual(self.example.keys(), ["key2", "key3", "key4"])

    def test_values(self):
        self.assertEqual(self.example.values(), ["value2", "value3", "value4"])

    def test_items(self):
        self.assertEqual(self.example.items(), [("key2", "value2"), ("key3", "value3"), ("key4", "value4")])

    def test_get(self):
        self.assertEqual(self.example.get("key2"), "value2")
        self.assertIsNone(self.example.get("non_existent"))

    def test_with_inputs(self):
        self.example = self.example.with_inputs("key2", "key3")
        self.assertEqual(self.example._input_keys, {"key2", "key3"})

    def test_inputs(self):
        self.assertEqual(self.example.inputs()._store, {"key2": "value2", "key3": "value3"})

    def test_labels(self):
        self.assertEqual(self.example.labels()._store, {"key4": "value4"})

    def test_iter(self):
        self.assertEqual(list(iter(self.example)), ["key2", "key3", "key4"])

    def test_copy(self):
        copied = self.example.copy()
        self.assertIsNot(copied, self.example)
        self.assertEqual(copied._store, self.example._store)

    def test_without(self):
        without_key2 = self.example.without("key2")
        self.assertNotIn("key2", without_key2)

    def test_toDict(self):
        self.assertEqual(self.example.toDict(), {"key2": "value2", "key3": "value3", "key4": "value4"})

if __name__ == "__main__":
    unittest.main()
