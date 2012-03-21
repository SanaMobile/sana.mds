'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 1.2
'''
import sys, traceback
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from piston.handler import BaseHandler
from piston import resource
from piston.utils import validate

from sana.api.models import *
from sana.api.responses import succeed, fail
from sana.mrs.util import enable_logging

class UnsupportedCRUDException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.value

class DispatchHandler(BaseHandler):
    """Base HTTP handler for Sana api. Uses basic CRUD approach of the  
       django-piston api as a thin wrapper around class specific functions.
    """
    @validate('POST')
    def create(self,request, *args, **kwargs):
        """ POST Request handler. Requires valid form defined by model of  
            extending class.
        """
        try:
            return succeed(self._create(request, args, kwargs))
        except:
            return self._trace(request, args, kwargs)
    
    def read(self,request, *args, **kwargs):
        """ GET Request handler. No validation is performed. """
        try:
            return succeed(self._read(request, args, kwargs))
        except:
            return self._trace(request, args, kwargs)
    
    def update(self, request, *args, **kwargs):
        """ POST Request handler. No validation is performed. """
        try:
            return succeed(self._update(request, args, kwargs))
        except:
            return self._trace(request, args, kwargs)
    
    def delete(self,request, *args, **kwargs):
        """ POST Request handler. No validation is performed. """
        try:
            return succeed(self._delete(request, args, kwargs))
        except:
            return self._trace(request, args, kwargs)

    # The CRUD methods
    @enable_logging
    def _create(self,request, *args, **kwargs):
        # Extending classes should use the following 
        # request.form.save()
        raise UnsupportedCRUDException('CREATE not supported')
    
    @enable_logging
    def _read(self,request, *args, **kwargs):
        raise UnsupportedCRUDException('READ not supported')
    
    @enable_logging
    def _update(self, request, *args, **kwargs):
        raise UnsupportedCRUDException('UPDATE not supported')
    
    @enable_logging
    def _delete(self,request, *args, **kwargs):
        raise UnsupportedCRUDException('DELETE not supported')

    @enable_logging
    def _trace(self,request, *args, **kwargs):
        et, val, tb = sys.exc_info()
        trace = traceback.format_tb(tb)
        error = {'error' : val, 'type': et, 'cause': trace[0]}
        for tbm in trace:
            logging.error(tbm)
        return fail(error)

class AuthHandler(BaseHandler):
    """ Handles auth requests. """
    allowed_methods = ('GET')
    def read(self,request, *args, **kwargs):
        pass
auth_resource = resource.Resource(AuthHandler)

class ConceptHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Concept
concept_resource = resource.Resource(ConceptHandler)

class DeviceHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Device
device_resource = resource.Resource(DeviceHandler)

class EncounterHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Encounter
encounter_resource = resource.Resource(EncounterHandler)

class NotificationHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Notification
notification_resource = resource.Resource(EncounterHandler)

class ObservationHandler(DispatchHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation
observation_resource = resource.Resource(ObservationHandler)
    
class ProcedureHandler(BaseHandler):
    allowed_methods = ('GET','POST')
    model = Procedure
procedure_resource = resource.Resource(ProcedureHandler)

class SubjectHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Subject
subject_resource = resource.Resource(SubjectHandler)

class WorkerHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('GET', 'POST')
    model = Worker
worker_resource = resource.Resource(WorkerHandler)