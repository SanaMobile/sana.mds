''' Core features of the Sana Mobile Dispatch Server

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
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _
from piston.utils import validate, rc, decorator
from django.contrib.auth import authenticate

from sana.api.responses import error, unauthorized, AUTH_SUCCESS, AUTH_FAILURE, AUTH_DISABLED

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



def version(): 
    return settings.API_VERSION

API_VERSION = {_('API'):settings.API_VERSION } 
API_CONFIG_ERROR = _('Incorrect dispatch configuration')


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
        if hasattr(klass, 'form'):
            # want to start encouraging use of form
            v_form = getattr(klass, 'form')
        elif hasattr(klass, 'v_form'):
            # old validate form,v-form, notation
            v_form = getattr(klass, 'v_form')
        elif hasattr(klass, 'model'):
            # try to create one on the fly
            v_form = modelform_factory(model=getattr(klass, 'model'))
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
    if request.method == "POST":
        uname = request.POST['username']
        pw = request.POST['password']
    else:
        uname = request.REQUEST.get("username",'')
        pw = request.REQUEST.get("password",'')
        
    result, msg = False, "Invalid auth. {uname}".format(uname=uname)
    # require non empty username and password    
    if uname and pw:
        user = authenticate(username=uname, password=pw)
        if user is not None:
            if user.is_active:
                result, msg = True, AUTH_SUCCESS.format(username=uname)
            else:
                result, msg = False, AUTH_DISABLED.format(username=uname)
        else:
            result, msg = False, AUTH_FAILURE.format(username=uname)
    return result, msg


    