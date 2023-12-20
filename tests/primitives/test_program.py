import unittest
from unittest.mock import MagicMock

from dspy.primitives.program import Program


class TestProgram(unittest.TestCase):
    def setUp(self):
        self.program = Program()

    def test_init(self):
        self.assertIsInstance(self.program, Program)

    def test_call(self):
        result = self.program()
        self.assertIsNone(result)

    def test_named_predictors(self):
        mock_predictor = MagicMock()
        self.program._predictor = mock_predictor
        self.assertEqual(self.program.named_predictors(), [('_predictor', mock_predictor)])

    def test_predictors(self):
        mock_predictor = MagicMock()
        self.program._predictor = mock_predictor
        self.assertEqual(self.program.predictors(), [mock_predictor])

    def test_repr(self):
        self.assertEqual(repr(self.program), "")

    def test_map_named_predictors(self):
        mock_predictor = MagicMock()
        self.program._predictor = mock_predictor
        self.program.map_named_predictors(lambda x: x)
        mock_predictor.assert_called_once()


if __name__ == "__main__":
    unittest.main()
