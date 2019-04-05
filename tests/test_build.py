import os

from unittest import TestCase

from no_drama.build import stage_bundle
from no_drama.context import temp_directory
from tests.helpers import Namespace, WorkInTemporaryDirectory


class TestBuild(WorkInTemporaryDirectory, TestCase):
    def setUp(self):
        super(TestBuild, self).setUp()
        self.test_data = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'build'
        )

    def make_build_args(self, force_build):
        return Namespace(
            project_path=os.path.join(self.test_data, 'sample_proj'),
            name='sample_proj',
            label='testing',
            r=[
                os.path.join(
                    self.test_data,
                    'sample_proj',
                    'requirements.txt'
                ),
            ],
            aux=[
                os.path.join(self.test_data, 'aux/1'),
                'aux2=%s' % os.path.join(self.test_data, 'aux/2'),
            ],
            static=[os.path.join(self.test_data, 'extra_static')],
            f=force_build
        )

    def test_build_creates_archive(self):
        archive_filename = os.path.join(
            os.getcwd(),
            'sample_proj_testing.zip'
        )

        self.assertFalse(os.path.exists(archive_filename))

        args = self.make_build_args(force_build=False)
        stage_bundle(args)

        self.assertTrue(os.path.exists(archive_filename))

    def test_build_skipped_if_archive_already_exists_and_no_force(self):
        archive_filename = os.path.join(
            os.getcwd(),
            'sample_proj_testing.zip'
        )

        with open(archive_filename, 'w') as f:
            f.write('archive already exists')

        self.assertTrue(os.path.exists(archive_filename))
        existing_stat = os.stat(archive_filename)

        args = self.make_build_args(force_build=False)
        stage_bundle(args)

        self.assertTrue(os.path.exists(archive_filename))
        self.assertEqual(os.stat(archive_filename), existing_stat)
