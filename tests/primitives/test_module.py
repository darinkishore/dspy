import unittest
from unittest.mock import MagicMock

from dspy.primitives.module import BaseModule


class TestBaseModule(unittest.TestCase):
    def setUp(self):
        self.module = BaseModule()

    def test_init(self):
        self.assertIsInstance(self.module, BaseModule)

    def test_named_parameters(self):
        mock_param = MagicMock()
        self.module._param = mock_param
        self.assertEqual(self.module.named_parameters(), [('_param', mock_param)])

    def test_parameters(self):
        mock_param = MagicMock()
        self.module._param = mock_param
        self.assertEqual(self.module.parameters(), [mock_param])

    def test_deepcopy(self):
        copy = self.module.deepcopy()
        self.assertEqual(copy, self.module)
        self.assertIsNot(copy, self.module)

    def test_reset_copy(self):
        copy = self.module.reset_copy()
        self.assertEqual(copy, self.module)
        self.assertIsNot(copy, self.module)
        self.assertTrue(copy._param.reset.called)

    def test_dump_state(self):
        mock_state = {'_param': 'state'}
        self.module._param = MagicMock()
        self.module._param.dump_state.return_value = 'state'
        self.assertEqual(self.module.dump_state(), mock_state)

    def test_load_state(self):
        mock_state = {'_param': 'state'}
        self.module._param = MagicMock()
        self.module.load_state(mock_state)
        self.module._param.load_state.assert_called_with('state')

    def test_save(self):
        mock_state = {'_param': 'state'}
        self.module._param = MagicMock()
        self.module._param.dump_state.return_value = 'state'
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.module.save('path')
            mock_file.assert_called_with('path', 'w')
            mock_file().write.assert_called_with(mock_state)

    def test_load(self):
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data='{"_param": "state"}')) as mock_file:
            self.module._param = MagicMock()
            self.module.load('path')
            mock_file.assert_called_with('path', 'r')
            self.module._param.load_state.assert_called_with('state')

if __name__ == "__main__":
    unittest.main()
