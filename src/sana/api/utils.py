'''
Created on Feb 29, 2012


:Authors: Sana Dev Team
:Version: 1.2
'''
import uuid

from django.conf import settings
from django.http import HttpResponse


LOGGING_ENABLE_ATTR = 'LOGGING_ENABLE'

def render_json_response(data):
    """Sends an HttpResponse with the X-JSON header and the right mimetype.
    
    Parameters:
        data
            message content
    """
    resp = HttpResponse(data, mimetype=("application/json; charset=" +
                                        settings.DEFAULT_CHARSET))
    resp['X-JSON'] = data
    return resp

def make_uuid():
    """ A utility to generate universally unique ids. """
    return str(uuid.uuid4())

def enable_logging(f):
    """ Decorator to enable logging on a Django request method.
    """
    def new_f(*args, **kwargs):
        request = args[0]
        setattr(request, LOGGING_ENABLE_ATTR, True)
        return f(*args, **kwargs)
    new_f.func_name = f.func_name
    return new_f