import unittest

from dspy.primitives.assertions import (assert_no_except_handler,
                                        assert_transform_module,
                                        bypass_assert_handler,
                                        bypass_suggest_handler,
                                        handle_assert_forward, noop_handler,
                                        suggest_backtrack_handler)


class TestAssertionHelpers(unittest.TestCase):
    def test_noop_handler(self):
        def func_raise_assertion():
            raise AssertionError

        def func_no_raise():
            return True

        self.assertIsNone(noop_handler(func_raise_assertion)())
        self.assertTrue(noop_handler(func_no_raise)())

    def test_bypass_suggest_handler(self):
        def func_raise_assertion():
            raise AssertionError

        def func_no_raise():
            return True

        with self.assertRaises(AssertionError):
            bypass_suggest_handler(func_raise_assertion)()
        self.assertTrue(bypass_suggest_handler(func_no_raise)())

    def test_bypass_assert_handler(self):
        def func_raise_assertion():
            raise AssertionError

        def func_no_raise():
            return True

        self.assertIsNone(bypass_assert_handler(func_raise_assertion)())
        self.assertTrue(bypass_assert_handler(func_no_raise)())

    def test_assert_no_except_handler(self):
        def func_raise_assertion():
            raise AssertionError

        def func_no_raise():
            return True

        self.assertIsNone(assert_no_except_handler(func_raise_assertion)())
        self.assertTrue(assert_no_except_handler(func_no_raise)())

    def test_suggest_backtrack_handler(self):
        def func_raise_suggestion_once():
            if not hasattr(func_raise_suggestion_once, "counter"):
                func_raise_suggestion_once.counter = 0
            func_raise_suggestion_once.counter += 1
            if func_raise_suggestion_once.counter == 1:
                raise AssertionError
            return True

        def func_raise_suggestion_twice():
            if not hasattr(func_raise_suggestion_twice, "counter"):
                func_raise_suggestion_twice.counter = 0
            func_raise_suggestion_twice.counter += 1
            if func_raise_suggestion_twice.counter <= 2:
                raise AssertionError
            return True

        def func_raise_suggestion_thrice():
            if not hasattr(func_raise_suggestion_thrice, "counter"):
                func_raise_suggestion_thrice.counter = 0
            func_raise_suggestion_thrice.counter += 1
            if func_raise_suggestion_thrice.counter <= 3:
                raise AssertionError
            return True

        self.assertTrue(suggest_backtrack_handler(func_raise_suggestion_once)())
        self.assertTrue(suggest_backtrack_handler(func_raise_suggestion_twice)())
        with self.assertRaises(AssertionError):
            suggest_backtrack_handler(func_raise_suggestion_thrice)()

    def test_handle_assert_forward(self):
        class DummyModule:
            def _forward(self, *args, **kwargs):
                return True

        dummy_module = DummyModule()
        self.assertTrue(handle_assert_forward(noop_handler)(dummy_module, "dummy")())

    def test_assert_transform_module(self):
        class DummyModule:
            def forward(self, *args, **kwargs):
                return True

        dummy_module = DummyModule()
        transformed_module = assert_transform_module(dummy_module)
        self.assertTrue(transformed_module.forward("dummy"))


if __name__ == "__main__":
    unittest.main()
