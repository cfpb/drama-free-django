import os
import shutil
import tempfile


# Replaced by types.SimpleNamespace in Python 3.3.
class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class WorkInTemporaryDirectory(object):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.previous_working_dir = os.getcwd()
        os.chdir(self.tempdir)

    def tearDown(self):
        os.chdir(self.previous_working_dir)
        shutil.rmtree(self.tempdir)
