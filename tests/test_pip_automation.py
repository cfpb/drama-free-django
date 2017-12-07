import unittest

# Some Python 2-friendly imports
try:
    import unittest.mock as mock
except ImportError:
    import mock

import no_drama.pip_automation as pip_automation


class TestPipAutomation(unittest.TestCase):

    @mock.patch('no_drama.pip_automation.pip.main')
    def test_save_wheels(self, mock_pip_main):
        mock_pip_main.return_value = 0
        pip_automation.save_wheels('/bootsrap_wheels', ['some', 'packages'],
                                   ['first.txt', 'second.txt'])
        self.assertEqual(mock_pip_main.call_count, 1)

    @mock.patch('no_drama.pip_automation.pip.main')
    def test_save_wheels_pip_failure(self, mock_pip_main):

        # Fail the first call to pip.main()
        mock_pip_main.reset_mock()
        mock_pip_main.side_effect = [1, 0]
        with self.assertRaises(ValueError):
            pip_automation.save_wheels('/bootsrap_wheels',
                                       ['some', 'packages'],
                                       ['first.txt', 'second.txt'])
            self.assertEqual(mock_pip_main.call_count, 1)
