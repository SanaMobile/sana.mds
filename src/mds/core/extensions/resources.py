from piston.resource import Resource
from .handlers import *

__all__ = [
    'rsrc_anm',
    'rsrc_patient',
    'rsrc_anmsession'
    ]
    
rsrc_anm = Resource(ANMHandler)
rsrc_patient = Resource(PatientHandler)
rsrc_anmsession = Resource(ANMSessionHandler)
