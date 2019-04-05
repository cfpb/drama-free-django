import os
from unittest import TestCase
from zipfile import ZipFile

from no_drama.release import inject_configuration
from tests.helpers import Namespace, WorkInTemporaryDirectory


class TestRelease(WorkInTemporaryDirectory, TestCase):
    def setUp(self):
        super(TestRelease, self).setUp()
        self.test_data = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'release'
        )

    def test_release_modifies_archive(self):
        args = Namespace(
            build_zip=os.path.join(self.test_data, 'archive.zip'),
            requirements_file=os.path.join(
                self.test_data,
                'extra-requirements.txt'
            ),
            vars=os.path.join(self.test_data, 'environment.json'),
            slug='release-testing',
            paths=os.path.join(self.test_data, 'paths.json'),
            prepend_wsgi=os.path.join(self.test_data, 'prepend-wsgi.py'),
            append_wsgi=os.path.join(self.test_data, 'append-wsgi.py'),
        )

        release_archive = './archive_release-testing.zip'
        self.assertFalse(os.path.exists(release_archive))

        inject_configuration(args)

        self.assertTrue(os.path.exists(release_archive))
        with ZipFile(release_archive, 'r') as zipfile:
            files = zipfile.namelist()

            # Extra wheel was installed from extra-requirements.txt.
            self.assertIn(
                'sample_proj/wheels/wagtail-1.13.4-py2.py3-none-any.whl',
                files
            )

            self.assertIn('sample_proj/environment.json', files)
            self.assertIn('sample_proj/paths.d/1_custom.json', files)
            self.assertIn('sample_proj/pre-wsgi.py-fragment', files)
            self.assertIn('sample_proj/post-wsgi.py-fragment', files)
