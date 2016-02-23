import os
import dfd_paths

real_settings = os.environ.get('REAL_DJANGO_SETTINGS')

if real_settings:
    exec("from %s  import *" % real_settings)

else:
    raise ImportError

DEBUG = False

if os.path.exists(dfd_paths.static_in):
    if 'STATICFILES_DIRS' in locals():
        STATICFILES_DIRS.append(dfd_paths.static_in)
    else:
        STATICFILES_DIRS = [dfd_paths.static_in]

STATIC_ROOT = dfd_paths.static_out
