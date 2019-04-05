from os.path import exists, isdir
from tempfile import gettempdir
from unittest import TestCase

from no_drama.context import temp_directory


class TestTempDirectory(TestCase):
    def test_temp_directory(self):
        with temp_directory() as tempdir:
            self.assertTrue(exists(tempdir))
            self.assertTrue(isdir(tempdir))
            self.assertTrue(tempdir.startswith(gettempdir()))
