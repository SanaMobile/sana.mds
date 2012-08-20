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

from sana.api.handlers import RESTHandler
from sana.api.decorators import logged
from sana.api.docs.utils import handler_uri_templates
from sana.api.models import RESTModel
from sana.api.responses import succeed, fail
from sana.core.models import *
from sana.core.signals import done_logging, signal_logger

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
           'SubjectHandler',]


__signals__ = ( done_logging, signal_logger)

class LogHandler(object):
    def __init__(self, model):
        self.model = RequestLog
        
    def __call__(self, **kwargs):
        return
     
    def save(self, **kwargs):
        self.instance = RequestLog(kwargs)
        
        
class AuthHandler(BaseHandler):
    """ Handles auth requests. """
    allowed_methods = ('GET',)
    
    def read(self,request):
        return http.HttpResponse(request.__dict__)
    
@logged
class ConceptHandler(RESTHandler):
    """ Handles concept requests. """
    allowed_methods = ('GET', 'POST')
    model = Concept
    signals = __signals__
    fields = ("uuid", "name")

class RelationshipHandler(RESTHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST')
    model = Relationship
    
class RelationshipCategoryHandler(RESTHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST')
    model = RelationshipCategory

class DeviceHandler(RESTHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST')
    model = Device
    
class EncounterHandler(RESTHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Encounter
    fields = ("uuid", "concept", "observation",'subject','procedure')
    #TODO wrap this around the old json.py

class NotificationHandler(RESTHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST')
    model = Notification
    #TODO wrap this around the old json.py

class ObservationHandler(RESTHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation
        
class ObserverHandler(RESTHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST')
    model = Observer
    
class ProcedureHandler(RESTHandler):
    allowed_methods = ('GET', 'POST')
    model = Procedure
    full = []
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
    signals = __signals__
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

   
class DocHandler(BaseHandler):
    """ Handles rest api documentation requests. """
    allowed_methods = ('GET',)
    documents = [EncounterHandler]
    
    #TODO fix this
    def read(self, request, *args, **kwargs):
        _handled = getattr(self.__class__, 'documents', [])
        return [ handler_uri_templates(x) for x in _handled]
        
        
    
