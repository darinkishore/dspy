import unittest

from dspy.primitives import assertions
from dspy.primitives.assertions import logging


class TestAssertions(unittest.TestCase):

    def test_setup_logger(self):
        logger = assertions.setup_logger()
        self.assertIsInstance(logger, logging.Logger)

    def test_build_error_msg(self):
        feedback_msgs = ["Error 1", "Error 2", "Error 3"]
        expected_msg = "\n".join(feedback_msgs)
        self.assertEqual(assertions._build_error_msg(feedback_msgs), expected_msg)

    def test_DSPyAssertionError(self):
        error = assertions.DSPyAssertionError("1", "Test error")
        self.assertEqual(error.id, "1")
        self.assertEqual(error.msg, "Test error")
        self.assertIsNone(error.state)

    def test_DSPySuggestionError(self):
        error = assertions.DSPySuggestionError("1", "Test error")
        self.assertEqual(error.id, "1")
        self.assertEqual(error.msg, "Test error")
        self.assertIsNone(error.target_module)
        self.assertIsNone(error.state)

    def test_Constraint(self):
        constraint = assertions.Constraint(True, "Test constraint")
        self.assertEqual(constraint.id, "1")
        self.assertEqual(constraint.msg, "Test constraint")
        self.assertIsNone(constraint.target_module)

    def test_Assert(self):
        assert_ = assertions.Assert(True, "Test assert")
        self.assertTrue(assert_())

    def test_Suggest(self):
        suggest = assertions.Suggest(True, "Test suggest")
        self.assertTrue(suggest())

    def test_noop_handler(self):
        @assertions.noop_handler
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_bypass_suggest_handler(self):
        @assertions.bypass_suggest_handler
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_bypass_assert_handler(self):
        @assertions.bypass_assert_handler
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_assert_no_except_handler(self):
        @assertions.assert_no_except_handler
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_suggest_backtrack_handler(self):
        @assertions.suggest_backtrack_handler
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_handle_assert_forward(self):
        @assertions.handle_assert_forward
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_default_assertion_handler(self):
        @assertions.default_assertion_handler
        def test_func():
            return True
        self.assertTrue(test_func())

    def test_assert_transform_module(self):
        class TestModule:
            def forward(self):
                return True
        module = TestModule()
        transformed_module = assertions.assert_transform_module(module)
        self.assertTrue(transformed_module.forward())

if __name__ == "__main__":
    unittest.main()
