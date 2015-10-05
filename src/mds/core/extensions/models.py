"""
The observer extensions for ssi models

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mds.api.utils import make_uuid
from mds.core.models.observer import Observer
from mds.core.models.subject import Subject
from mds.core.models.encounter import Encounter


__all__ = [
    'EncounterReview',
    'SurgicalAdvocate',
    'Surgeon',
    'SurgicalSubject',
]

# Extend observer class
class Surgeon(Observer):
    """ Extension of Observer class representing individuals
        performing surgical operations.
    """
    class Meta:
        app_label = "core"
        verbose_name = 'surgeon'
        
    device = models.ForeignKey('core.Device', blank=True)
    email = models.EmailField(_('email'), blank=True)
    
    @property
    def number(self):
        return self.device.name if self.device else "990009999"
        
class SurgicalAdvocate(Observer):
    """ Extension of Observer class representing workers
        who will perform in home follow up visits
    """
    class Meta:
        app_label = "core"
        verbose_name = 'surgical advocate'
        
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
        verbose_name = 'surgical subject'

    def __unicode__(self):
        return u'%s, %s - %s' % (self.family_name, self.given_name, self.system_id)

    house_number = models.CharField(_('house number'), max_length=64, blank=True)
    family_number = models.IntegerField(_('family number'),max_length=5, null=True, blank=True)
    national_id = models.IntegerField(_('national id'),max_length=7, null=True, blank=True)
    contact_one =  models.CharField(_('conctact one'),max_length=64, blank=True)
    contact_two =  models.CharField(_('contact two'),max_length=64, blank=True)
    contact_three =  models.CharField(_('telephone number three'),max_length=64, blank=True)
    contact_four =  models.CharField(_('telephone number four'),max_length=64, blank=True)
    confirmed = models.BooleanField(_('confirmed'),default=True)

class EncounterReview(models.Model):

    class Meta:
        app_label = "core"
        verbose_name = 'encounter review'

    uuid = models.SlugField(max_length=36, 
        unique=True, default=make_uuid, editable=False)
    """ A universally unique identifier """

    encounter = models.ForeignKey(Encounter, 
        to_field='uuid',
        verbose_name=_('encounter'))
    """Who the task is assigned to"""

    reviewed_by = models.ForeignKey(Observer, 
        to_field='uuid',
        verbose_name=_('reviewed by'))
    """Who the task is assigned to"""

    viewed_on = models.DateTimeField(_('viewed on'),
        auto_now_add=True)
    """ updated on modification """

    completed = models.DateTimeField(_('completed'),
        blank=True)
    """ When the review was completed """
