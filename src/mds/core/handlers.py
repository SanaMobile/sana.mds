'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
import cjson

from django.contrib.auth import authenticate

from piston.handler import BaseHandler
from piston.resource import Resource

from mds.api import do_authenticate, LOGGER
from mds.api.handlers import DispatchingHandler
from mds.api.decorators import logged, validate
from mds.api.docs.utils import handler_uri_templates
from mds.api.responses import succeed, fail, error
from mds.api.signals import EventSignal, EventSignalHandler

from .forms import *
from .models import *

__all__ = ['ConceptHandler', 
           'RelationshipHandler',
           'RelationshipCategoryHandler',
           'DeviceHandler', 
           'EncounterHandler',
           'EventHandler',
           'LocationHandler',
           'NotificationHandler', 
           'ObservationHandler', 
           'ObserverHandler',
           'ProcedureHandler',
           'DocHandler' ,
           'SessionHandler',
           'SubjectHandler',]

   
@logged     
class SessionHandler(DispatchingHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

    def create(self,request):
        username = request.REQUEST.get('username', 'empty')
        password = request.REQUEST.get('password','empty')
        user = authenticate(username=username, password=password)
        try:
            success,msg = do_authenticate(request)
            #if success:
            #    return succeed(msg)
            if user is not None:
                observer = Observer.objects.get(user=user)
                return succeed(observer.uuid)
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
    fields = (
        "uuid",
        "name",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged    
class EncounterHandler(DispatchingHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Encounter
    form = EncounterForm
    fields = ("uuid",
        "concept", 
        "observation",
        ("subject",("uuid",)),
        "created",
        "modified",
        ("procedure",("title","uuid")),
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class EventHandler(BaseHandler):
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

@logged
class ObservationHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation
    form = ObservationForm
    fields = (
        "uuid",
        ("encounter",("uuid")),
        "node",
        ("concept",("uuid",)),
        "value_text",
        "value_complex",
        "value",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged        
class ObserverHandler(DispatchingHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST')
    model = Observer
    form = ObserverForm
    fields = ("uuid",
              ("user",("username","is_superuser")),
             )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ProcedureHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST')
    model = Procedure
    fields = ("uuid",
              "title",
              "description",
              "src",
              "version",
              "author",
             )
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
    fields = (
        "uuid",
        "family_name",
        "given_name",
        "gender",
        "dob",
        "image",
        "system_id",
        ("location",("name","uuid")),
    )
    model = Subject
    form = SubjectForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

class DocHandler(BaseHandler):
    """ Handles rest api documentation requests. """
    allowed_methods = ('GET',)
    documents = [EncounterHandler]
    
    #TODO fix this
    def read(self, request, *args, **kwargs):
        _handled = getattr(self.__class__, 'documents', [])
        return [ handler_uri_templates(x) for x in _handled]
        
# new stuff
class LocationHandler(DispatchingHandler):
    model = Location
    fields = ("name","uuid","code")

class CompoundFormHandler(object):
    forms = {}
    """ A list of 2-tuples representing the names and forms on the page """
    allowed_methods = ('POST',)
    
