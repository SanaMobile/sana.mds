'''
Created on Aug 10, 2012

:author: Sana Development Team
:version: 2.0
'''
try:
    import json as simplejson
except ImportError, e:
    import simplejson
import sys, traceback
import logging

from django.conf import settings
from django.forms import ValidationError
from piston.handler import BaseHandler

from sana.core.handlers import RequestLogHandler as BaseRequestHandler

from sana.api.contrib.openmrs import openmrs16 as openmrs
from sana.api.responses import succeed, fail
from sana.api.decorators import logged

from sana.api.v1.json import render_json_response, MSG_MDS_ERROR
from sana.api.v1.json import notification_submit, register_client_events
from sana.api.v1.json import binary_submit, binarychunk_submit, binarychunk_hack_submit
from sana.api.v1.json import patient_get, patient_list

from sana.api.v1.api import register_saved_procedure
from sana.mrs.forms import ProcedureSubmitForm
from sana.mrs.models import RequestLog

from sana.api.signals import EventSignal
from sana.mrs.signals import event_signalhandler 

@logged
class AuthHandler(BaseHandler):
    """ Handles status and authentication check requests. For working with
        openMRS versions 1.6+
    """
    allowed_methods = ('GET',)
    logger = (event_signalhandler, EventSignal())
    
    def read(self,request, *args, **kwargs):
        """Validates user credentials with the backing data store.

         Request parameters:
            username
                a valid username
            password
                a valid password

         Parameters:
            request
                An authorization check request.
        """
        try:
            username = request.REQUEST.get("username", None)
            password = request.REQUEST.get("password", None)
            logging.info("username %s" % username)
            omrs = openmrs.OpenMRS(username, password,
                              settings.OPENMRS_SERVER_URL)
            if omrs.validate_credentials(username, password):
                response = succeed("username and password validated!")
            else:
                response = fail("username and password combination incorrect!")
            logging.debug(response)
        except Exception, e:
            msg = 'validate_credentials' #% MSG_MDS_ERROR
            logging.error('%s %s' % (msg, str(e)))
            response = fail(msg)
        return response
    
@logged   
class SavedProcedureHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('POST')
    logger = (event_signalhandler, EventSignal())
    
    def create(self,request, *args, **kwargs):
        logging.info("Received saved procedure submission.")
        response = ''
        form = ProcedureSubmitForm(request.POST)
        try:
            form.full_clean()
            savedproc_guid  = form.cleaned_data['savedproc_guid']
            procedure_guid = form.cleaned_data['procedure_guid']
            responses = form.cleaned_data['responses']
            phone = form.cleaned_data['phone']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            result, message = register_saved_procedure(savedproc_guid,
                                                       procedure_guid,
                                                       responses,
                                                       phone,
                                                       username,
                                                       password)
            if result:
                response = succeed("Successfully saved the procedure: %s" % message)
                logging.info("Saved procedure successfully registered.")
            else:
                response = fail(message)
                logging.error("Failed to register procedure: %s" % message)
        except ValidationError, v:
            for k,v in form._get_errors().items():
                logging.error("SavedProcedure argument %s:%s" % (k,v))
            response = fail("Invalid ProcedureSubmitForm data")
            raise Exception('Saved procedure submission was invalid')
    
        except Exception, e:
            et, val, tb = sys.exc_info()
            trace = traceback.format_tb(tb)
            error = "Exception : %s %s %s" % (et, val, trace[0])
            for tbm in trace:
                logging.error(tbm)
            response = fail(error)
        return response

class EventHandler(BaseHandler):
    
    def create(self,request, *args, **kwargs):
        """Accepts a request for submitting client events.
        
        Request Parameters:
            client_id 
                The client phone number
            events 
                The client events
            
        Events should be submitted as a list in JSON formatted text with each 
        event having the following key/value pairs:
        
        Event
            event_type
                An event type
            event_value 
                An event value
            event_time 
                The time of the event in milliseconds since epoch
            encounter_reference 
                The encounter, or saved procedure, id
            patient_reference
                The patient id
            user_reference 
                TODO
        
        Parameters:
            request
                The client event log request.
        """
    
        client_id = request.REQUEST.get('client_id', None)
        events_json = request.REQUEST.get('events', None)
    
        if events_json is None or client_id is None:
            return render_json_response(fail("Could not parse eventlog submission."))
    
        logging.info("Received events parameter: %s" % events_json)
    
        try:
            events = simplejson.loads(events_json)
            result, message = register_client_events(client_id, events)
    
            response = None
            if result:
                response = succeed(message)
            else:
                response = fail(message)
        except Exception, e:
            logging.error("Error while processing events: %s" % e)
            response = fail("Could not parse eventlog submission.")
        return render_json_response(response)

class RequestLogHandler(BaseRequestHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST')
    model = RequestLog
    
@logged    
class NotificationHandler(BaseHandler):
    """ Handles encounter requests. """
    allowed_methods = ('POST')
    logger = (event_signalhandler, EventSignal())
    
    def create(self,request, *args, **kwargs):
        return notification_submit(request) 
    
@logged
class BinaryHandler(BaseHandler):
    allowed_methods = ('POST')
    logger = (event_signalhandler, EventSignal())
    
    def create(self,request, *args, **kwargs):
        return binary_submit(request)
    
@logged
class BinaryPacketHandler(BaseHandler):
    allowed_methods = ('POST')
    logger = (event_signalhandler, EventSignal())
    
    def create(self,request, *args, **kwargs):
        return binarychunk_submit(request)
    
@logged
class Base64PacketHandler(BaseHandler):
    allowed_methods = ('POST')
    logger = (event_signalhandler, EventSignal())
    
    def create(self,request, *args, **kwargs):
        return binarychunk_hack_submit(request)
    

@logged
class PatientHandler(BaseHandler):
    """ Handles patient requests. """
    allowed_methods = ('GET',)
    logger = (event_signalhandler, EventSignal())
    
    def read(self,request, id=None, **kwargs):
        if id and id != 'list':
            return patient_get(request,id)
        else:
            return patient_list(request)
        
    def create(self,request, *args, **kwargs):
        pass
    
    def _read(self,request, *args, **kwargs):
        if args:
            return patient_get(request, args[0])
        else:
            return patient_list(request)