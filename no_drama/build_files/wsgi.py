import os

import sitecustomize
import dfd_paths

from django.core.servers.basehttp import get_internal_wsgi_application

application = get_internal_wsgi_application()

if os.path.exists(dfd_paths.extended_wsgi):
    execfile(dfd_paths.extended_wsgi)
