from __future__ import print_function

import os
import json
import sys

from glob import glob

this_file = os.path.realpath(__file__)
this_dir = os.path.dirname(this_file)
root = os.path.realpath(os.path.join(this_dir, '../'))

paths = {'environment': 'environment.json',
         'static_in': '../../static.in',
         'build_static_in' : 'static.in',
         'extended_python_path': '../../lib',
         'static_out': 'static',
         'update_symlink': '../../current',
         'debug_if_exists': '../../DEBUG',
         'pre_wsgi': 'pre-wsgi.py-fragment',
         'post_wsgi': 'post-wsgi.py-fragment',
         'build_lib': 'lib',
         'aux':'aux',
         'root':'.'
         }

pathfiles_glob = os.path.join(root, 'paths.d/*.json')

pathfiles = [open(p) for p in glob(pathfiles_glob)]

for pathfile in pathfiles:
    new_paths = json.load(pathfile)
    paths.update(new_paths)
    pathfile.close()


def get_path(name):
    relpath = paths[name]
    if relpath is not None and bool(relpath) is True:
        joined = os.path.join(root, relpath)
        return os.path.normpath(joined)
    else:
        raise KeyError('no path found for %s' % name)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Lookup paths in a drama-free-django"
                                     " release")

    parser.add_argument('key')

    args = parser.parse_args()

    try:
        print(get_path(args.key))
    except KeyError:
        print("we have no path named: ", args.key, file=sys.stderr)
