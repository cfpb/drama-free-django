#!/usr/bin/env python

import sys
import argparse
from os.path import abspath

from no_drama import builder


parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('output', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
parser.add_argument('--type', default='run_module_name',
                    choices=['run_module_name', 'run_module_path',
                             'run_console_script', 'import_module_name'])
parser.add_argument('--environment-type', default='system',
                    choices=['system', 'pex', 'virtualenv'])
parser.add_argument('--environment-path',
                    help="path to virtualenv or pex file", type=abspath)
parser.add_argument('--vars', help="path(s) to JSON-encoded environment"
                                   "variables", type=abspath, nargs="*")
parser.add_argument('--paths', help="prepend path(s) to sys.path", nargs="*",
                    type=abspath)
parser.add_argument('--python', help="path to python executable",
                    default='/usr/bin/env python')

def main():
    args = parser.parse_args()
    builder.build(args)


if __name__ == '__main__':
    main()
