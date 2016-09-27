import unittest

# Some Python 2-friendly imports
try:
    import unittest.mock as mock
except ImportError:
    import mock

import no_drama.pip_automation as pip_automation


class TestPipAutomation(unittest.TestCase):

    def test_hash_for_path(self):
        with mock.patch('no_drama.pip_automation.open',
                mock.mock_open(read_data='testtest'), create=True):
            result = pip_automation.hash_for_path('/test-path')
            self.assertEqual(result,
                    '51abb9636078defbf888d8457a7c76f85c8f114c')

    @mock.patch('no_drama.pip_automation.hash_for_path')
    def test_cache_marker_for_path(self, mock_hash_for_path):
        mock_hash_for_path.return_value = \
                '51abb9636078defbf888d8457a7c76f85c8f114c'
        result = pip_automation.cache_marker_for_path('/test-path')
        self.assertEqual(result,
                'requirements_hashes/51abb9636078defbf888d8457a7c76f85c8f114c')

    @mock.patch('os.path.exists')
    @mock.patch('no_drama.pip_automation.cache_marker_for_path')
    def test_is_cache_update_required_false(self, 
            mock_cache_marker_for_path, mock_os_path_exists):
        mock_cache_marker_for_path.return_value = \
                'requirements_hashes/51abb9636078defbf888d8457a7c76f85c8f114c'
        mock_os_path_exists.return_value = True
        result = pip_automation.is_cache_update_required('/test-path')
        self.assertFalse(result)

    @mock.patch('os.path.exists')
    @mock.patch('no_drama.pip_automation.cache_marker_for_path')
    def test_is_cache_update_required_true(self, 
            mock_cache_marker_for_path, mock_os_path_exists):
        mock_cache_marker_for_path.return_value = \
                'requirements_hashes/51abb9636078defbf888d8457a7c76f85c8f114c'
        mock_os_path_exists.return_value = False
        result = pip_automation.is_cache_update_required('/test-path')
        self.assertTrue(result)

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    @mock.patch('no_drama.pip_automation.cache_marker_for_path')
    def test_record_req_cached_dir_does_not_exist(self, 
            mock_cache_marker_for_path, mock_os_path_exists, mock_os_mkdir):
        mock_cache_marker_for_path.return_value = \
                'requirements_hashes/51abb9636078defbf888d8457a7c76f85c8f114c'
        mock_os_path_exists.return_value = False

        mock_open_mock = mock.mock_open()
        with mock.patch('no_drama.pip_automation.open', 
                mock_open_mock, create=True):
            result = pip_automation.record_req_cached('/test-path')

        mock_open_mock().write.assert_called_once_with('')
        self.assertTrue(mock_os_mkdir.called)

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists')
    @mock.patch('no_drama.pip_automation.cache_marker_for_path')
    def test_record_req_cached_dir_exists(self, 
            mock_cache_marker_for_path, mock_os_path_exists, mock_os_mkdir):
        mock_cache_marker_for_path.return_value = \
                'requirements_hashes/51abb9636078defbf888d8457a7c76f85c8f114c'
        mock_os_path_exists.return_value = True

        mock_open_mock = mock.mock_open()
        with mock.patch('no_drama.pip_automation.open', 
                mock_open_mock, create=True):
            result = pip_automation.record_req_cached('/test-path')

        mock_open_mock().write.assert_called_once_with('')
        self.assertFalse(mock_os_mkdir.called)

    @mock.patch('no_drama.pip_automation.is_cache_update_required')
    @mock.patch('no_drama.pip_automation.record_req_cached')
    @mock.patch('no_drama.pip_automation.pip.main')
    def test_save_wheels(self, mock_pip_main,
            mock_record_req_cached, mock_is_cache_update_required):
        mock_is_cache_update_required.return_value = False
        mock_pip_main.return_value = 0
        pip_automation.save_wheels('/bootsrap_wheels', ['some', 'packages'], 
                ['first.txt', 'second.txt'])
        self.assertEqual(mock_pip_main.call_count, 2)

    @mock.patch('no_drama.pip_automation.is_cache_update_required')
    @mock.patch('no_drama.pip_automation.record_req_cached')
    @mock.patch('no_drama.pip_automation.pip.main')
    def test_save_wheels_pip_failure(self, mock_pip_main,
            mock_record_req_cached, mock_is_cache_update_required):
        mock_is_cache_update_required.return_value = False

        # Fail the second call to pip.main()
        mock_pip_main.side_effect = [0, 1]
        with self.assertRaises(ValueError):
            pip_automation.save_wheels('/bootsrap_wheels', ['some', 'packages'], 
                    ['first.txt', 'second.txt'])
            self.assertEqual(mock_pip_main.call_count, 2)

        # Fail the first call to pip.main()
        mock_pip_main.reset_mock()
        mock_pip_main.side_effect = [1, 0]
        with self.assertRaises(ValueError):
            pip_automation.save_wheels('/bootsrap_wheels', ['some', 'packages'], 
                    ['first.txt', 'second.txt'])
            self.assertEqual(mock_pip_main.call_count, 1)
