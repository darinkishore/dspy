import unittest

from dspy.primitives.prediction import Completions, Prediction


class TestPrediction(unittest.TestCase):
    def setUp(self):
        self.prediction = Prediction(base={"key1": "value1", "key2": "value2"}, key3="value3")

    def test_init(self):
        self.assertEqual(self.prediction._store, {"key1": "value1", "key2": "value2", "key3": "value3"})
        self.assertIsNone(self.prediction._demos)
        self.assertIsNone(self.prediction._input_keys)
        self.assertIsNone(self.prediction._completions)

    def test_from_completions(self):
        completions = {"key1": ["value1", "value2"], "key2": ["value3", "value4"]}
        prediction = Prediction.from_completions(completions)
        self.assertEqual(prediction._store, {"key1": "value1", "key2": "value3"})
        self.assertEqual(prediction._completions._completions, completions)

    def test_repr(self):
        self.assertEqual(repr(self.prediction), "Prediction(\n    key1=value1,\n    key2=value2,\n    key3=value3\n)")

    def test_str(self):
        self.assertEqual(str(self.prediction), "Prediction(\n    key1=value1,\n    key2=value2,\n    key3=value3\n)")

    def test_completions(self):
        self.assertIsNone(self.prediction.completions)


class TestCompletions(unittest.TestCase):
    def setUp(self):
        self.completions = Completions({"key1": ["value1", "value2"], "key2": ["value3", "value4"]})

    def test_init(self):
        self.assertEqual(self.completions._completions, {"key1": ["value1", "value2"], "key2": ["value3", "value4"]})
        self.assertIsNone(self.completions.signature)

    def test_items(self):
        self.assertEqual(list(self.completions.items()), [("key1", ["value1", "value2"]), ("key2", ["value3", "value4"])])

    def test_getitem(self):
        self.assertEqual(self.completions[0]._store, {"key1": "value1", "key2": "value3"})
        self.assertEqual(self.completions["key1"], ["value1", "value2"])

    def test_getattr(self):
        self.assertEqual(self.completions.key1, ["value1", "value2"])

    def test_len(self):
        self.assertEqual(len(self.completions), 2)

    def test_contains(self):
        self.assertTrue("key1" in self.completions)
        self.assertFalse("key3" in self.completions)

    def test_repr(self):
        self.assertEqual(repr(self.completions), "Completions(\n    key1=['value1', 'value2'],\n    key2=['value3', 'value4']\n)")

    def test_str(self):
        self.assertEqual(str(self.completions), "Completions(\n    key1=['value1', 'value2'],\n    key2=['value3', 'value4']\n)")


if __name__ == "__main__":
    unittest.main()
