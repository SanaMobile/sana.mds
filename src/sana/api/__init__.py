'''
Core features of the Sana Mobile Dispatch Server

Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
try:
    import json
except ImportError:
    import simplejson as json
import logging

from django.core.urlresolvers import get_resolver, get_callable, get_script_prefix, reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from piston.utils import validate, rc, decorator
from django.contrib.auth import authenticate

SIGNALS = 'signals'


# Logging constants
LOG_SIGNAL = 'logger'
LOGGING_ENABLED = 'LOGGING_ENABLE'
LOGGING_START = 'LOGGING_START_TIME'

VERBOSITY = ('SUMMARY', 'DETAIL','VERBOSE')

CRITICAL = 32
FATAL = CRITICAL
ERROR = 16
WARNING = 8
WARN = WARNING
INFO = 4
DEBUG = 2
NOTSET = 0

LOG_LEVELS = { 'CRITICAL': 32,
           'FATAL' : CRITICAL,
           'ERROR' : 16,
           'WARNING' : 8,
           'WARN' : WARNING,
           'INFO' : 4,
           'DEBUG' : 2,
           'NOTSET' : 0 }
LEVEL_CHOICES = ((16, 'ERROR'),(16,'WARN'),('INFO' , 4),('DEBUG',2),('NOTSET',0))

CRUD = ("POST", "GET","PUT","DELETE")
crud = ("create", "read","update","delete")

# version strings
_MAJOR_VERSION = '2'
_MINOR_VERSION = '0'

#__all__ = ['version', 'fail', 'succeed', 'validate', 'do_authenticate',
#           'API_VERSION' ]

def version(): 
    return settings.API_VERSION

API_VERSION = {_('API'):settings.API_VERSION } 
API_CONFIG_ERROR = _('Incorrect dispatch configuration')



def fail(data):
    ''' Fail response as a python dict with data '''
    response = {'status': 'FAILURE',
                'message': data}
    return response

def succeed(data):
    ''' Success response as a python dict with data '''
    response = {'status': 'SUCCESS',
                'message': data}
    return response

def error(data):
    return fail(data)

def validate(operation='POST'):
    ''' Adds the following attributes to all CRUD requests
        
        Request.FORM         => the raw dispatchable content
        Request.CONTENT      => the dispatchable object
        
        Adds the following to the form
        Request.FORMAT       => the output format
        
        The Request.$VALUE are field names taken from api.fields module.
        
        This implementation requires all requests to have valid form data.
    '''
    @decorator
    def wrap(f, handler, request, *a, **kwa):
        # gets the form we will validate
        klass = handler.__class__
        if hasattr(klass, 'v_form'):
            v_form = getattr(klass, 'v_form')
        else:
            return error(u'Invalid object')
        # Create the dispatchable form and validate
        if operation == 'POST':
            data = getattr(request, operation)
            form = v_form(data=data)
            if not form.is_valid():
                errs = dict((key, [unicode(v) for v in values]) for key,values in form.errors.items())
                return error(errs)
        else:
            data = handler.flatten_dict(getattr(request, operation))
            form = v_form(data=data,empty_permitted=True)
        setattr(request, 'form', form)
        return f(handler, request, *a, **kwa)
    return wrap

def do_authenticate(request):
    """ Performs a user authentication check and returns one of the following:
    
        True, "username and password validated!"
        False, "Disabled account."
        False, "username and password combination incorrect!"
        
        Requires the request have "username" and "password" parameters
        Parameters:
            request
                the request to authenticate
    """
    uname = ''
    pw = ''
    result, msg = False, "username and password combination incorrect!"
    if request.method == "POST":
        uname = request.POST['username']
        pw = request.POST['password']
    else:
        uname = request.REQUEST.get("username",'')
        pw = request.REQUEST.get("password",'')
    logging.info("Authentication attempt from user: %s" % uname)
    # require non empty username and password    
    if uname and pw:
        user = authenticate(username=uname, password=pw)
        if user is not None:
            if user.is_active:
                result, msg = True, "username and password validated!"
            else:
                result, msg = False, "Disabled account."
        else:
            result, msg = False, ""
    return result, msg


    