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
         'build_static_in': 'static.in',
         'extended_python_path': '../../lib',
         'static_out': 'static',
         'update_symlink': '../../current',
         'persistent_media_root': '../../MEDIA_ROOT',
         'secret_key': '../../SECRET_KEY',
         'pre_wsgi': 'pre-wsgi.py-fragment',
         'post_wsgi': 'post-wsgi.py-fragment',
         'build_lib': 'lib',
         'aux': 'aux',
         'root': '.'
         }

pathfiles_glob = os.path.join(root, 'paths.d/*.json')

pathfiles = [open(p) for p in glob(pathfiles_glob)]

for pathfile in pathfiles:
    new_paths = json.load(pathfile)
    paths.update(new_paths)
    pathfile.close()


def make_path(relpath):
    return os.path.normpath(os.path.join(root, relpath))


def get_path(name):
    relpath = paths.get(name)

    if not relpath:
        raise KeyError('no path found for %s' % name)

    return make_path(relpath)

def get_path_if_exists(name):
    if name not in paths:
        raise KeyError('no path found for %s' % name)

    relpath = paths[name]

    if relpath:
        path = make_path(relpath)

        if os.path.exists(path):
            return path


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
