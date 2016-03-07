import os
import dfd

real_settings = os.environ.get('REAL_DJANGO_SETTINGS')

if real_settings:
    exec("from %s  import *" % real_settings)

else:
    raise ImportError

DEBUG = False

static_in = dfd.get_path('static_in')
static_out = dfd.get_path('static_out')

if static_in and os.path.exists(static_in):
    if 'STATICFILES_DIRS' in locals():
        STATICFILES_DIRS.append(static_in)
    else:
        STATICFILES_DIRS = [static_in]

STATIC_ROOT = static_out
