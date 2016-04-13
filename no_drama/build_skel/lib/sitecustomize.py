import os
import json

import dfd

extended_python_path = dfd.get_path_if_exists(extended_python_path')
environment_path = dfd.get_path_if_exists('environment')

if extended_python_path:
    import site
    site.addsitedir(extended_python_path)

if environment_path:
    with open(environment_path) as env_file:
        new_env_vars = json.load(env_file)

        resolved_paths = {key: dfd.get_path(key) for key in dfd.paths}

        # this allows environment variables to be relative to named paths
        interpolated = {key: value.format(**resolved_paths)
                        for key, value in new_env_vars.items()}

        os.environ.update(interpolated)

real_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
if real_settings is not None:
    os.environ['REAL_DJANGO_SETTINGS'] = real_settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dfd_settings'
