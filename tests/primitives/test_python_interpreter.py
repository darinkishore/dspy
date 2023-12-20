import unittest
from unittest.mock import MagicMock

from dspy.primitives.python_interpreter import (CodePrompt, PythonInterpreter,
                                                TextPrompt)


class TestPythonInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = PythonInterpreter(action_space={"mock_func": MagicMock()}, import_white_list=["math"])

    def test_init(self):
        self.assertEqual(self.interpreter.action_space, {"mock_func": MagicMock()})
        self.assertEqual(self.interpreter.import_white_list, ["math"])

    def test_execute(self):
        code = "mock_func()"
        self.interpreter.execute(code)
        self.interpreter.action_space["mock_func"].assert_called_once()

    def test_clear_state(self):
        self.interpreter.clear_state()
        self.assertEqual(self.interpreter.state, {"mock_func": MagicMock()})
        self.assertEqual(self.interpreter.fuzz_state, {})

    # Additional test cases for the private methods...

class TestTextPrompt(unittest.TestCase):
    def setUp(self):
        self.prompt = TextPrompt("This is a test prompt.")

    def test_key_words(self):
        self.assertEqual(self.prompt.key_words, {"test", "prompt"})

    def test_format(self):
        formatted_prompt = self.prompt.format(test="mock_test")
        self.assertEqual(formatted_prompt, "This is a mock_test prompt.")

class TestCodePrompt(unittest.TestCase):
    def setUp(self):
        self.prompt = CodePrompt("This is a test code prompt.", code_type="python")

    def test_code_type(self):
        self.assertEqual(self.prompt.code_type, "python")

    def test_set_code_type(self):
        self.prompt.set_code_type("java")
        self.assertEqual(self.prompt.code_type, "java")

    def test_execute(self):
        interpreter = MagicMock()
        result, used_interpreter = self.prompt.execute(interpreter)
        self.assertEqual(result, None)
        self.assertEqual(used_interpreter, interpreter)

if __name__ == "__main__":
    unittest.main()
