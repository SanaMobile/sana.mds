'''
Response definitions.

Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 1.2
'''
import cjson
try:
    import json
except ImportError:
    import simplejson as json
import logging

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from piston.utils import validate, rc, decorator

API_VERSION = {_('API'): getattr(settings, 'API_VERSION', "") } 
API_CONFIG_ERROR = _('Incorrect dispatch configuration')


def fail(data):
    ''' Fail response as a python dict with data '''
    response = {'status': 'FAILURE',
                'data': data}
    return response

def succeed(data):
    ''' Success response as a python dict with data '''
    response = {'status': 'SUCCESS',
                'data': data}
    return response