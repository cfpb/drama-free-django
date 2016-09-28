import subprocess
import unittest

# Some Python 2-friendly imports
try:
    import unittest.mock as mock
except ImportError:
    import mock

import no_drama.executable as executable


class TestExecutable(unittest.TestCase):

    @mock.patch('shutil.move')
    @mock.patch('zipfile.ZipFile')
    @mock.patch('os.stat')
    @mock.patch('os.chmod')
    @mock.patch('os.unlink')
    def test_make_executable(self,
            mock_os_unlink,
            mock_os_chmod,
            mock_os_stat,
            mock_zipfile,
            mock_shutil_move):
        mock_os_stat.return_value = [33188,]

        mock_open_mock = mock.mock_open()
        with mock.patch('no_drama.executable.open',
                mock_open_mock, create=True):
            executable.make_executable('/path/archive.zip', 'build-number-1')

        # Make sure all our external calls are good
        mock_shutil_move.assert_called_with('/path/archive.zip',
                '/path/archive.zip_')
        mock_zipfile.assert_called_with('/path/archive.zip_', 'a')
        mock_os_stat.assert_called_with('/path/archive.zip')
        mock_os_chmod.assert_called_with('/path/archive.zip', 33261)
        mock_os_unlink.assert_called_with('/path/archive.zip_')

        # Inspect the contents of the zipfile
        mock_zipfile_instance = mock_zipfile()
        zipfile_args = mock_zipfile_instance.writestr.call_args[0]
        self.assertEqual(len(zipfile_args), 2)
        self.assertIn('build-number-1', zipfile_args[1])

    @mock.patch('os.getcwd')
    @mock.patch('zipfile.ZipFile')
    @mock.patch('os.chdir')
    @mock.patch('subprocess.check_call')
    def test_self_extraction_script(self, mock_subprocess_check_call,
            mock_os_chdir, mock_zipfile, mock_os_getcwd):
        """ This attempts to test the self-extraction script. Because
            it's a string that gets written to a file, we have to exec
            it here to test. We'll slice out the function we're
            interested in, deploy_to(), and test just that. This is a
            bit hacky. """
        mock_os_getcwd.return_value = '/some-path'

        # This should build the self-extraction script, then exec it into 
        # the local namespace.
        prefix = 'build-number-1'
        script_string = executable.self_extraction_script.format(prefix=prefix)
        script_obj = compile(script_string, '__main__.py', 'exec')
        exec(script_obj, globals())

        deploy_to('archive.zip', '/deployment-path')

        mock_zipfile.assert_called_with('/some-path/archive.zip')
        mock_subprocess_check_call.assert_called_with(
                ['sh', '/deployment-path/build-number-1/activate.sh'])

        # Try again with a failure
        mock_subprocess_check_call.reset_calls()
        mock_subprocess_check_call.side_effect = \
                subprocess.CalledProcessError(1, 'sh', '')
        with self.assertRaises(subprocess.CalledProcessError):
            deploy_to('archive.zip', '/deployment-path')
