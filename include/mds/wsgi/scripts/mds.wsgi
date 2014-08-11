# WSGI config file for serving mds
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mds.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
path = '/var/local/www/mds'
if path not in sys.path:
    sys.path.append(path)

