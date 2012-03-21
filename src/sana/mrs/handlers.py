"""
HTTP Request handlers using Piston API.

:Authors: Sana dev team
:Version: 1.2
"""

from django.utils.translation import ugettext_lazy as _

from piston.handler import BaseHandler
from piston import resource
from piston.utils import validate

from sana.api.handlers import DispatchHandler
from sana.mrs.json import validate_credentials, binarychunk_submit
from sana.mrs.json import binarychunk_hack_submit, procedure_submit
from sana.mrs.json import saved_procedure_get, patient_get, patient_list
from sana.mrs.json import notification_submit, binary_submit

from sana.mrs.models import *
from sana.mrs.util import enable_logging


class AuthHandler(DispatchHandler):
    """ Handles status and authentication check requests. """
    allowed_methods = ('GET')
    
    def _read(self,request, *args, **kwargs):
        return validate_credentials(request)   
auth_resource = resource.Resource(AuthHandler)

class BinaryHandler(BaseHandler):
    allowed_methods = ('POST')
    def create(self,request, *args, **kwargs):
        return binary_submit(request)
binary_resource = resource.Resource(BinaryHandler)

class BinaryPacketHandler(BaseHandler):
    allowed_methods = ('POST')
    def create(self,request, *args, **kwargs):
        return binarychunk_submit(request)
packet_resource = resource.Resource(BinaryPacketHandler)

class Base64PacketHandler(BaseHandler):
    allowed_methods = ('POST')
    def create(self,request, *args, **kwargs):
        return binarychunk_hack_submit(request)
base64_resource = resource.Resource(Base64PacketHandler)

class SavedProcedureHandler(DispatchHandler):
    """ Handles encounter requests. """
    allowed_methods = ('POST')
    model = SavedProcedure
    def create(self,request, *args, **kwargs):
        return procedure_submit(request)
    
    def read(self,request, *args):
        return saved_procedure_get(request, args[0])
    
encounter_resource = resource.Resource(SavedProcedureHandler)

class PatientHandler(DispatchHandler):
    """ Handles patient requests. """
    allowed_methods = ('GET')
    model = Patient
    
    def _read(self,request, *args, **kwargs):
        if args:
            return patient_get(request, args[0])
        else:
            return patient_list(request)
            
patient_resource = resource.Resource(PatientHandler)

class ProcedureHandler(DispatchHandler):
    allowed_methods = ('GET','POST')
    model = Procedure
procedure_resource = resource.Resource(ProcedureHandler)

class NotificationHandler(DispatchHandler):
    """ Handles encounter requests. """
    allowed_methods = ('POST')
    model = Notification
    
    def create(self,request, *args, **kwargs):
        return notification_submit(request)
notification_resource = resource.Resource(NotificationHandler)

class StatusHandler(BaseHandler):
    """ Handles status and authentication check requests. """
    allowed_methods = ('GET')

    def _read(self,request, *args, **kwargs):
        return validate_credentials(request)   
status_resource = resource.Resource(StatusHandler)
