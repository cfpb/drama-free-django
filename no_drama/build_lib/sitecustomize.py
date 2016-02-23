import os
import json

import dfd_paths

if os.path.exists(dfd_paths.environment):
    with open(dfd_paths.environment) as env_file:
        new_env_vars = json.load(env_file)
        os.environ.update(new_env_vars)

real_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
if real_settings is not None:
    os.environ['REAL_DJANGO_SETTINGS'] = real_settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dfd_settings'
