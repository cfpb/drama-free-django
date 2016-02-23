import os
import json

this_file = os.path.realpath(__file__)
this_dir = os.path.dirname(this_file)
root = os.path.realpath(os.path.join(this_dir, '../'))

path_file_path = os.path.join(root, 'paths.json')

paths = {'environment': 'environment.json',
         'static_in': '../../static.in',
         'extended_python_path': '../../lib',
         'static_out': 'static',
         'update_symlink': '../../current',
         }

if os.path.exists(path_file_path):
    with open(path_file_path) as path_file:
        configured_paths = json.load(path_file)
        paths.update(configured_paths)


def abs_path(name):
    relpath = paths[name]
    if relpath is not None and bool(relpath) is True:
        joined = os.path.join(root, relpath)
        return os.path.normpath(joined)
    else:
        return None

environment = abs_path('environment')
static_in = abs_path('static_in')
static_out = abs_path('static_out')
extended_python_path = abs_path('extended_python_path')
update_symlink = abs_path('update_symlink')
