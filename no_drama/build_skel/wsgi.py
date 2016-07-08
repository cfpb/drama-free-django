import os

import sitecustomize
import dfd

from django.core.servers.basehttp import get_internal_wsgi_application

pre_wsgi = dfd.get_path('pre_wsgi')
post_wsgi = dfd.get_path('post_wsgi')

if pre_wsgi and os.path.exists(pre_wsgi):
    execfile(pre_wsgi)

application = get_internal_wsgi_application()

if post_wsgi and os.path.exists(post_wsgi):
    execfile(post_wsgi)
