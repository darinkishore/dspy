import unittest
from unittest.mock import Mock

import openai
from dsp.evaluation import utils


class TestUtils(unittest.TestCase):
    def test_evaluateRetrieval(self):
        mock_fn = Mock(return_value=Mock(context="context", answer="answer"))
        mock_dev = [Mock(question="question", answer="answer")]

        if openai.__version__ >= '1.0':
            result = utils.evaluateRetrieval(mock_fn, mock_dev)
            self.assertEqual(result, 100.0)
        else:
            result = utils.evaluateRetrieval(mock_fn, mock_dev)
            self.assertEqual(result, 100.0)

    def test_evaluateAnswer(self):
        mock_fn = Mock(return_value=Mock(answer="answer"))
        mock_dev = [Mock(question="question", answer="answer")]

        if openai.__version__ >= '1.0':
            result = utils.evaluateAnswer(mock_fn, mock_dev)
            self.assertEqual(result, 100.0)
        else:
            result = utils.evaluateAnswer(mock_fn, mock_dev)
            self.assertEqual(result, 100.0)

    def test_evaluate(self):
        mock_fn = Mock(return_value=Mock(answer="answer"))
        mock_dev = [Mock(question="question", answer="answer")]

        if openai.__version__ >= '1.0':
            result = utils.evaluate(mock_fn, mock_dev)
            self.assertEqual(result, 100.0)
        else:
            result = utils.evaluate(mock_fn, mock_dev)
            self.assertEqual(result, 100.0)

if __name__ == '__main__':
    unittest.main()
