'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
import cjson

from piston.handler import BaseHandler

from sana.api import do_authenticate, LOGGER
from sana.api.handlers import RESTHandler
from sana.api.decorators import logged, validate
from sana.api.docs.utils import handler_uri_templates
from sana.api.responses import succeed, fail, error
from sana.api.signals import EventSignal, EventSignalHandler

from sana.core.forms import *
from sana.core.models import *

__all__ = ['ConceptHandler', 
           'RelationshipHandler',
           'RelationshipCategoryHandler',
           'DeviceHandler', 
           'EncounterHandler', 
           'NotificationHandler', 
           'ObservationHandler', 
           'ObserverHandler',
           'ProcedureHandler',
           'RequestLogHandler',
           'DocHandler' ,
           'SessionHandler',
           'SubjectHandler',]

class LogHandler(object):
    def __init__(self, model):
        self.model = RequestLog
        
    def __call__(self, **kwargs):
        return
     
    def save(self, **kwargs):
        self.instance = RequestLog(kwargs)
        
@logged     
class SessionHandler(RESTHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    
    def create(self,request):
        try:
            success,msg = do_authenticate(request)
            if success:
                return succeed(msg)
            else:
                logging.warn(msg)
                return fail(msg)
        except:
            msg = "Internal Server Error"
            logging.error(msg)
            return error(msg)
        
    def read(self,request):
        success,msg = do_authenticate(request)
        if success:
            return succeed(msg)
        else:
            return fail(msg)
    
@logged
class ConceptHandler(RESTHandler):
    """ Handles concept requests. """
    allowed_methods = ('GET', 'POST')
    model = Concept
    form = ConceptForm
    fields = ("uuid", "name")
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}

class RelationshipHandler(RESTHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST')
    model = Relationship
    form = RelationshipForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    
class RelationshipCategoryHandler(RESTHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST')
    model = RelationshipCategory
    form = RelationshipCategoryForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}

@logged
class DeviceHandler(RESTHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST')
    model = Device
    form = DeviceForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    
@logged    
class EncounterHandler(RESTHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Encounter
    form = EncounterForm
    fields = ("uuid", "concept", "observation",'subject','procedure')
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    #TODO wrap this around the old json.py

@logged
class NotificationHandler(RESTHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST')
    model = Notification
    form = NotificationForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    #TODO wrap this around the old json.py

@logged
class ObservationHandler(RESTHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation
    form = ObservationForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    
@logged        
class ObserverHandler(RESTHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST')
    model = Observer
    form = ObserverForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}

@logged
class ProcedureHandler(RESTHandler):
    allowed_methods = ('GET', 'POST')
    model = Procedure
    form = ProcedureForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}
    
    def _read_by_uuid(self,request,uuid):
        """ Returns the procedure file instead of the verbose representation on 
            uuid GET requests 
        """
        model = getattr(self.__class__, 'model')
        obj =  model.objects.get(uuid=uuid)
        return open(obj.src.path).read()
    
class RequestLogHandler(RESTHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST')
    model = RequestLog

@logged
class SubjectHandler(RESTHandler):
    """ Handles subject requests. """
    allowed_methods = ('GET', 'POST')
    fields = ['uuid']
    model = Subject
    form = SubjectForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(RequestLog))}

   
class DocHandler(BaseHandler):
    """ Handles rest api documentation requests. """
    allowed_methods = ('GET',)
    documents = [EncounterHandler]
    
    #TODO fix this
    def read(self, request, *args, **kwargs):
        _handled = getattr(self.__class__, 'documents', [])
        return [ handler_uri_templates(x) for x in _handled]
        
        
    
