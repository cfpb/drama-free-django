import sys
import unittest

import mock

from no_drama.pip_automation import save_wheels


class TestPipAutomation(unittest.TestCase):
    @mock.patch('subprocess.check_call')
    def test_save_wheels_calls_pip_wheel(self, check_call):
        save_wheels(
            '/destination/path',
            packages=['django', 'wagtail'],
            requirements_paths=['requirements/base.txt', 'extra.txt']
        )

        check_call.assert_called_once_with([
            sys.executable,
            '-m',
            'pip',
            'wheel',
            '--wheel-dir=/destination/path',
            'django',
            'wagtail',
            '-rrequirements/base.txt',
            '-rextra.txt',
        ])

    @mock.patch('subprocess.check_call', side_effect=RuntimeError)
    def test_save_wheels_raises_pip_wheel_exception(self, check_call):
        with self.assertRaises(RuntimeError):
            save_wheels('/destination/path')
