'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
#must import the local module models for the handlers
from .models import *
from sana.api import LOGGER
from sana.core import handlers
from sana.api.decorators import logged
from sana.api.signals import EventSignal, EventSignalHandler

__all__ = ['ConceptHandler', 'RelationshipHandler','RelationshipCategoryHandler',
           'DeviceHandler', 
           'EncounterHandler', 
           'NotificationHandler', 
           'ObservationHandler', 
           'ObserverHandler',
           'ProcedureHandler',
           'EventHandler',
           'SessionHandler',
           'SubjectHandler',]

@logged     
class SessionHandler(handlers.SessionHandler):
    """ Handles session auth requests. """
    allowed_methods = ('GET','POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
        
@logged
class ConceptHandler(handlers.ConceptHandler):
    """ Handles concept requests. """
    allowed_methods = ('GET', 'POST')
    model = Concept
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class RelationshipHandler(handlers.RelationshipHandler):
    """ Handles concept relationship requests. """
    allowed_methods = ('GET', 'POST')
    model = Relationship
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged
class RelationshipCategoryHandler(handlers.RelationshipCategoryHandler):
    """ Handles concept relationship category requests. """
    allowed_methods = ('GET', 'POST')
    model = RelationshipCategory
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}


@logged
class DeviceHandler(handlers.DeviceHandler):
    """ Handles device requests. """
    allowed_methods = ('GET', 'POST')
    model = Device
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class EncounterHandler(handlers.EncounterHandler):
    """ Handles encounter requests. """
    model = Encounter
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

class EventHandler(handlers.EventHandler):
    """ Handles network request log requests. """
    allowed_methods = ('GET', 'POST')
    model = Event

@logged
class NotificationHandler(handlers.NotificationHandler):
    """ Handles notification requests. """
    allowed_methods = ('GET', 'POST')
    model = Notification
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class ObservationHandler(handlers.ObservationHandler):
    allowed_methods = ('GET', 'POST')
    model = Observation

@logged 
class ObserverHandler(handlers.ObserverHandler):
    """ Handles observer requests. """
    allowed_methods = ('GET', 'POST')
    model = Observer
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
@logged
class ProcedureHandler(handlers.ProcedureHandler):
    allowed_methods = ('GET', 'POST')
    model = Procedure
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}


@logged
class SubjectHandler(handlers.SubjectHandler):
    """ Handles subject requests. """
    model = Subject
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

    
    
