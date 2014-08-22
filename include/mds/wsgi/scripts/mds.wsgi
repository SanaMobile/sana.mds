# WSGI config file for serving mds
import os
import sys

path = '/var/local/webapps'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mds.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


