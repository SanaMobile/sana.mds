'''
Created on Aug 9, 2012

:author: Sana Development Team
:version: 2.0
'''

from sana.api import LOGGING_ENABLED, LOG_SIGNAL, SIGNALS
from django.core.signals import request_finished, got_request_exception, Signal
from django.db import models
from sana.api import CRUD, crud
from sana.api.utils import make_uuid, dictzip

def enable_logging(f):
    """ Decorator to enable logging on a Django request method.
    """
    def new_f(*args, **kwargs):
        request = args[0]
        setattr(request, LOGGING_ENABLED, True)
        return f(*args, **kwargs)
    new_f.func_name = f.func_name
    return new_f


CRUD_MAP = dictzip(CRUD,crud)


def logged(klazz):
    """ Decorator to enable logging on a Piston Handler classes CRUD methods.
        Checks for the 'allowed_methods' class attribute to determine which
        methods to log. 
    """
    def _enable(f):
        def new_f(*args, **kwargs):
            request = args[1]
            signals = getattr(klazz, SIGNALS, None)
            callback = None
            signal = None
            if isinstance(signals, tuple):
                signal,callback = signals
            elif isinstance(signals, Signal):
                signal = signals
                callback = request_finished
                
            if signal and callback:
                signal.connect(callback)
            setattr(request, LOG_SIGNAL, signal)
            setattr(request, LOGGING_ENABLED, True)
            return f(*args, **kwargs)
        new_f.func_name = f.func_name
        return new_f
    # wraps each of the methods declared in the classes 
    # allowed_methods class to enable logging
    methods = getattr(klazz,'allowed_methods',[])
    for m in methods:
        attr = CRUD_MAP.get(m,None)
        f = getattr(klazz, attr)
        if f:
            setattr(klazz, attr, _enable(f))
    return klazz 

def universal(klazz):
    """ Decorator that declares a unique name field to a Model class. """
    field = models.CharField(max_length=36, unique=True,
                             default = make_uuid,
                             primary_key=True)
    setattr(klazz,'uuid',field)

def cacheable(klazz):
    """ Decorator that declares a unique name field to a Model class. """
    field = models.TextField(blank=True)
    setattr(klazz,'cache',field)