'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
import cjson

from piston.handler import BaseHandler

from sana.api import do_authenticate, LOGGER
from sana.api.handlers import DispatchingHandler
from sana.api.decorators import logged, validate
from sana.api.docs.utils import handler_uri_templates
from sana.api.responses import succeed, fail, error
from sana.api.signals import EventSignal, EventSignalHandler

from .forms import *
from .models import *

__all__ = ['ConceptHandler', 
           'RelationshipHandler',
           'RelationshipCategoryHandler',
           'DeviceHandler', 
           'EncounterHandler',
           'EventHandler',
           'NotificationHandler', 
           'ObservationHandler', 
           'ObserverHandler',
           'ProcedureHandler',
           'DocHandler' ,
           'SessionHandler',
           'PatientHandler',]

   
@logged     
class SessionHandler(DispatchingHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
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
class ConceptHandler(DispatchingHandler):
    """ Handles concept requests. """
    allowed_methods = ('GET', 'POST')
    model = Concept
    form = ConceptForm
    fields = ("uuid", "name")
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

class RelationshipHandler(DispatchingHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST')
    model = Relationship
    form = RelationshipForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
class RelationshipCategoryHandler(DispatchingHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST')
    model = RelationshipCategory
    form = RelationshipCategoryForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class DeviceHandler(DispatchingHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST')
    model = Device
    form = DeviceForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged    
class EncounterHandler(DispatchingHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Encounter
    form = EncounterForm
    fields = ("uuid", "concept", "observation",'subject','procedure')
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    #TODO wrap this around the old json.py

class EventHandler(DispatchingHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST')
    model = Event

@logged
class NotificationHandler(DispatchingHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST')
    model = Notification
    form = NotificationForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    #TODO wrap this around the old json.py

@logged
class ObservationHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation
    form = ObservationForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged        
class ObserverHandler(DispatchingHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST')
    model = Observer
    form = ObserverForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ProcedureHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST')
    model = Procedure
    form = ProcedureForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
    def _read_by_uuid(self,request,uuid):
        """ Returns the procedure file instead of the verbose representation on 
            uuid GET requests 
        """
        model = getattr(self.__class__, 'model')
        obj =  model.objects.get(uuid=uuid)
        return open(obj.src.path).read()

@logged
class SubjectHandler(DispatchingHandler):
    """ Handles subject requests. """
    allowed_methods = ('GET', 'POST')
    fields = ['uuid']
    model = Patient
    form = PatientForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

   
class DocHandler(BaseHandler):
    """ Handles rest api documentation requests. """
    allowed_methods = ('GET',)
    documents = [EncounterHandler]
    
    #TODO fix this
    def read(self, request, *args, **kwargs):
        _handled = getattr(self.__class__, 'documents', [])
        return [ handler_uri_templates(x) for x in _handled]
        
        
    
