import os
import json

import dfd

extended_python_path = dfd.get_path_if_exists('extended_python_path')
environment_path = dfd.get_path_if_exists('environment')

if extended_python_path:
    import site
    site.addsitedir(extended_python_path)

if environment_path:
    with open(environment_path) as env_file:
        new_env_vars = json.load(env_file)
        os.environ.update(new_env_vars)

real_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
if real_settings is not None:
    os.environ['REAL_DJANGO_SETTINGS'] = real_settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dfd_settings'
