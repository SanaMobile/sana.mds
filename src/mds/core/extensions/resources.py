from piston.resource import Resource
from .handlers import *

__all__ = [
    'rsrc_anm',
    'rsrc_patient'
    ]
    
rsrc_anm = Resource(ANMHandler)
rsrc_patient = Resource(PatientHandler)
