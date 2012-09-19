'''
Created on Aug 7, 2012

@author: Sana Dev Team
'''
from django.db import models

from sana.core.models.concept import Concept as BaseConcept
from sana.core.models.concept import Relationship as BaseRelationship
from sana.core.models.concept import Relationship as BaseRelationshipCategory
from sana.core.models.device import Device as BaseDevice
from sana.core.models.encounter import Encounter  as BaseEncounter
from sana.core.models.events import Event as BaseEvent
from sana.core.models.notification import Notification as BaseNotification
from sana.core.models.observation import Observation  as BaseObservation
from sana.core.models.observer import Observer as BaseObserver
from sana.core.models.procedure import Procedure as BaseProcedure
from sana.core.models.subject import Subject as BaseSubject

__all__ = ['Concept', 'Relationship','RelationshipCategory',
           'Device', 
           'Encounter', 
           'Event',
           'Notification',
           'Observation', 
           'Observer',
           'Procedure',
           'Subject',]

_app = 'mds'

class Concept(BaseConcept):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseConcept, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")


class Relationship(BaseRelationship):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseRelationship, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")


class RelationshipCategory(BaseRelationshipCategory):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseRelationshipCategory, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")


class Device(BaseDevice):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseDevice, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")


class Encounter(BaseEncounter):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseEncounter, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")

class Event(BaseEvent):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseEvent, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")
    
class Notification(BaseNotification):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseNotification, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")

class Observation(BaseObservation):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseObservation, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")

class Observer(BaseObserver):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseObserver, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")

class Procedure(BaseProcedure):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseProcedure, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")

class Subject(BaseSubject):
    class Meta:
        app_label = _app
    parent_ptr = models.OneToOneField(BaseSubject, parent_link=True,
                             related_name="%(app_label)s_%(class)s_related")
