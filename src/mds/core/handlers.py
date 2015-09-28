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
           'SubjectHandler',
           'LocationHandler',]

   
@logged     
class SessionHandler(DispatchingHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    form = SessionForm
    #model = None
    
    def create(self,request):
        #data = self.flatten_dict(request.POST)
        '''
        is_json = request.META.get('CONTENT_TYPE', False)
        if is_json and is_json == 'application/json':
            #data = cjson.decode(request.body)
            username = data.get('username', None)
            password = data.get('password', None)
        else:
            username = request.REQUEST.get('username', 'empty')
            password = request.REQUEST.get('password','empty')
        '''
        #data = self.flatten_dict(request.POST)
        try:
            content_type = request.META.get('CONTENT_TYPE', None)
            logging.debug(content_type)
            is_json = 'json' in content_type
            logging.debug("is_json: %s" % is_json)
            if is_json:
                logging.debug("is_json = True")
                raw_data = request.read()
                data = cjson.decode(raw_data)
            else:
                data = self.flatten_dict(request.POST)
            username = data.get('username', 'empty')
            password = data.get('password','empty')
            user = authenticate(username=username, password=password)
            if user is not None:
                observer = Observer.objects.get(user=user)
                return succeed(observer.uuid)
            else:
                msg = "Invalid credentials"
                logging.warn(msg)
                return fail(msg)
        except Exception as e:
            msg = "Internal Server Error"
            logging.error(unicode(e))
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
    allowed_methods = ('GET', 'POST','PUT')
    model = Concept
    form = ConceptForm
    #fields = ("uuid", "name")
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

class RelationshipHandler(DispatchingHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Relationship
    form = RelationshipForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
class RelationshipCategoryHandler(DispatchingHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = RelationshipCategory
    form = RelationshipCategoryForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class DeviceHandler(DispatchingHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Device
    form = DeviceForm
    #fields = (
    #    "uuid",
    #    "name",
    #)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged    
class EncounterHandler(DispatchingHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Encounter
    form = EncounterForm
    #fields = ("uuid",
    #    "concept", 
    #    "observation",
    #    ("subject",("uuid",)),
    #    "created",
    #    "modified",
    #    ("procedure",("title","uuid")),
    #)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class EventHandler(BaseHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Event

@logged
class NotificationHandler(DispatchingHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Notification
    form = NotificationForm
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ObservationHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = Observation
    form = ObservationForm
    '''
    fields = (
        "uuid",
        ("encounter",("uuid")),
        "node",
        ("concept",("uuid",)),
        "value_text",
        "value_complex",
        "value",
    )
    '''
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged        
class ObserverHandler(DispatchingHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST','PUT')
    model = Observer
    form = ObserverForm
    '''
    fields = ("uuid",
              ("user",("username","is_superuser")),
             )
    '''
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ProcedureHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = Procedure
    '''
    fields = ("uuid",
              "title",
              "description",
              "src",
              "version",
              "author",
             )
    '''
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
    allowed_methods = ('GET', 'POST','PUT')
    '''
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
    '''
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
@logged
class LocationHandler(DispatchingHandler):
    model = Location
    fields = (
        "name",
        "uuid",
        "code"
    )

class CompoundFormHandler(object):
    forms = {}
    """ A list of 2-tuples representing the names and forms on the page """
    allowed_methods = ('POST',)
    
    def create(request, *args, **kwargs):
        cleaned = {}
        for k,v in getattr(self.__class__, "forms", {}).items():
            form = v(request.ITEMS[k])
            form.full_clean()
            cleaned[k] = form
            
    def __call__(self):
        pass

def intake_handler(request,*args,**kwargs):
    pass




