"""
The observer extensions for ssi models

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models

from mds.api.utils import make_uuid
from mds.core.models.observer import Observer
from mds.core.models.subject import Subject

__all__ = [
    'SurgicalAdvocate',
    'Surgeon',
    'SurgicalSubject',
]

# Extend observer class
class Surgeon(Observer):
    class Meta:
        app_label = "core"
    """ Extension of Observer class representing individuals
        performing surgical operations.
    """
    device = models.ForeignKey('core.Device',blank=True)
    email = models.EmailField(blank=True)
    @property
    def number(self):
        return self.device.name if self.device else "990009999"
        
class SurgicalAdvocate(Observer):
    class Meta:
        app_label = "core"
    """ Extension of Observer class representing workers
        who will perform in home follow up visits
    """
    device = models.ForeignKey('core.Device', blank=True)
    location = models.ForeignKey('core.Location',blank=True)
    
    @property
    def number(self):
        return self.device.name if self.device else "990009999"

    @property
    def location_code(self):
        return self.location.code if self.location else "00000000"

    def __unicode__(self):
        return u'%s - %s' % (self.location_code,self.user)

class SurgicalSubject(Subject):
    class Meta:
        app_label = "core"

    def __unicode__(self):
        return u'%s, %s - %s' % (self.family_name, self.given_name, self.system_id)

    house_number = models.CharField(max_length=64, blank=True)
    family_number = models.IntegerField(max_length=5, null=True, blank=True)
    national_id = models.IntegerField(max_length=7, null=True, blank=True)
    contact_one =  models.CharField(max_length=64, blank=True)
    contact_two =  models.CharField(max_length=64, blank=True)
    contact_three =  models.CharField(max_length=64, blank=True)
    contact_four =  models.CharField(max_length=64, blank=True)
