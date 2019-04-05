#!/usr/bin/env python

import argparse
import sys

from no_drama.build import stage_bundle
from no_drama.release import inject_configuration


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="drama-free deployable django projects"
    )

    subparsers = parser.add_subparsers()
    build_parser = subparsers.add_parser('build')
    release_parser = subparsers.add_parser('release')

    # build parser arguments
    build_parser.add_argument('project_path')

    build_parser.add_argument('name', help="name of this project")

    build_parser.add_argument('label', help="a label for this build-- "
                              "maybe a build ID or version number")

    build_parser.add_argument('-r', action='append', help="just like you would"
                              " 'pip install -r'")

    build_parser.add_argument('--aux', action='append',
                              help='extra directories to include, in form'
                              ' name=/path/to/dir.')

    build_parser.add_argument(
        '--static',
        action='append',
        help='extra directories to include in static files'
        'to be served from STATIC_ROOT')

    build_parser.add_argument(
        '-f',
        action='store_true',
        help="ignore if this build already exists")

    build_parser.set_defaults(func=stage_bundle)

    # release parser arguments
    release_parser.add_argument('build_zip', help='path to a zip file'
                                " generated with 'no-drama build'")
    release_parser.add_argument(
        'vars', help="JSON dictionary of env variables")
    release_parser.add_argument('slug', help="a label for this release")

    release_parser.add_argument('--paths', help="json file for overriding"
                                " default paths")
    release_parser.add_argument(
        '--requirements_file', help="just like you would"
        " 'pip install -r'. Let's you add more wheels to the build")

    release_parser.add_argument(
        '--prepend-wsgi',
        help="text file w/ additional python code to modify "
        "the environment before the wsgi 'application' is"
        " created")

    release_parser.add_argument(
        '--append-wsgi',
        help="text file w/ additional python code to modify "
        "the wsgi 'application'")

    release_parser.set_defaults(func=inject_configuration)

    parsed = parser.parse_args(args)

    # This logic is only necessary due to this change in Python 3:
    # https://bugs.python.org/issue16308
    if not hasattr(parsed, 'func'):  # pragma: no cover
        parser.print_help(sys.stderr)
        sys.exit(2)

    return parsed.func, parsed


def main():  # pragma: no cover
    func, args = parse_args()
    return func(args)


if __name__ == '__main__':
    main()
