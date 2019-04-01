from unittest import TestCase

from no_drama.__main__ import parse_args


class ArgParsingTests(TestCase):
    def test_argument_parsing_fails_without_any_args(self):
        try:
            parse_args([])
        except SystemExit as e:
            pass
        else:
            self.fail('At least one arg is required')

    def test_argument_parsing_build(self):
        func, args = parse_args([
            'build',
            '/path/to/code',
            'name',
            'label',
            '-r', 'req1.txt',
            '-r', 'req2.txt',
            '--aux', 'extra1',
            '--aux', 'extra2',
            '--static', 'static1',
            '--static', 'static2',
            '-f'
        ])

        self.assertEqual(args.project_path, '/path/to/code')
        self.assertEqual(args.name, 'name')
        self.assertEqual(args.label, 'label')
        self.assertEqual(args.r, ['req1.txt', 'req2.txt'])
        self.assertEqual(args.aux, ['extra1', 'extra2'])
        self.assertEqual(args.static, ['static1', 'static2'])
        self.assertTrue(args.f)

    def test_argument_parsing_release(self):
        func, args = parse_args([
            'release',
            '/path/to/archive.zip',
            'input_vars.json',
            'slug',
            '--paths', 'paths.json',
            '--requirements_file', 'reqs.txt',
            '--prepend-wsgi', 'prepend-wsgi.py',
            '--append-wsgi', 'append-wsgi.py',
        ])

        self.assertEqual(args.build_zip, '/path/to/archive.zip')
        self.assertEqual(args.vars, 'input_vars.json')
        self.assertEqual(args.slug, 'slug')
        self.assertEqual(args.paths, 'paths.json')
        self.assertEqual(args.requirements_file, 'reqs.txt')
        self.assertEqual(args.prepend_wsgi, 'prepend-wsgi.py')
        self.assertEqual(args.append_wsgi, 'append-wsgi.py')
