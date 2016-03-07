import os
import json

import dfd

environment_path = dfd.get_path('environment')

if os.path.exists(environment_path):
    with open(environment_path) as env_file:
        new_env_vars = json.load(env_file)
        os.environ.update(new_env_vars)

real_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
if real_settings is not None:
    os.environ['REAL_DJANGO_SETTINGS'] = real_settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dfd_settings'
