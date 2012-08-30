'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
import sys, traceback
import logging
import cjson

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django import http
from django.utils.translation import ugettext_lazy as _


from piston.handler import BaseHandler
from piston import doc

from sana.api import do_authenticate
from sana.api.handlers import RESTHandler
from sana.api.decorators import logged
from sana.api.docs.utils import handler_uri_templates
from sana.api.responses import succeed, fail, error

from sana.core.forms import *
from sana.core.models import *
from sana.core.signals import done_logging, event_signalhandler

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


__signals__ = ( done_logging, event_signalhandler)

class LogHandler(object):
    def __init__(self, model):
        self.model = RequestLog
        
    def __call__(self, **kwargs):
        return
     
    def save(self, **kwargs):
        self.instance = RequestLog(kwargs)
        
        
class SessionHandler(BaseHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = ( done_logging, event_signalhandler)
    logger = ( done_logging, event_signalhandler)
    
    def create(self,request):
        try:
            success,msg = do_authenticate(request)
            if success:
                return succeed(msg)
            else:
                return fail(msg)
        except:
            return error("Internal Server Error")
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
    signals = ( done_logging, event_signalhandler)
    logger = ( done_logging, event_signalhandler)
    fields = ("uuid", "name")

class RelationshipHandler(RESTHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST')
    model = Relationship
    form = RelationshipForm
    
class RelationshipCategoryHandler(RESTHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST')
    model = RelationshipCategory
    form = RelationshipCategoryForm

class DeviceHandler(RESTHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST')
    model = Device
    form = DeviceForm
    
class EncounterHandler(RESTHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Encounter
    form = EncounterForm
    fields = ("uuid", "concept", "observation",'subject','procedure')
    #TODO wrap this around the old json.py

class NotificationHandler(RESTHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST')
    model = Notification
    form = NotificationForm
    #TODO wrap this around the old json.py

class ObservationHandler(RESTHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation
    form = ObservationForm
        
class ObserverHandler(RESTHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST')
    model = Observer
    form = ObserverForm
    
class ProcedureHandler(RESTHandler):
    allowed_methods = ('GET', 'POST')
    model = Procedure
    form = ProcedureForm
    default_rep = ['uuid','author','version', 'name']
    
    def readByUuid(self,request,uuid):
        """ Returns the procedure file instead of the verbose representation on 
            uuid GET requests 
        """
        model = getattr(self.__class__, 'model')  
        return open(model.objects.get(uuid=uuid).src.path).read()
    
class RequestLogHandler(RESTHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST')
    model = RequestLog
    signals = ( done_logging, event_signalhandler)
    logger = ( done_logging, event_signalhandler)
    """    
    def readByUuid(self,request,uuid):
        log = self.queryset(request).get(uuid=uuid)
        message = {'id': uuid,
                    'data': cjson.decode(log.message,True)}
        
        return HttpResponse(cjson.encode(message))
    """


    

class SubjectHandler(RESTHandler):
    """ Handles subject requests. """
    allowed_methods = ('GET', 'POST')
    fields = ['uuid']
    model = Subject
    form = SubjectForm
    signals = ( done_logging, event_signalhandler)
    logger = ( done_logging, event_signalhandler)

   
class DocHandler(BaseHandler):
    """ Handles rest api documentation requests. """
    allowed_methods = ('GET',)
    documents = [EncounterHandler]
    
    #TODO fix this
    def read(self, request, *args, **kwargs):
        _handled = getattr(self.__class__, 'documents', [])
        return [ handler_uri_templates(x) for x in _handled]
        
        
    
