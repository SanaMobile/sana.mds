"""
Extensions for core models

:Authors: Sana dev team
:Version: 2.0
"""
from django.db import models
from django.utils import timezone
 
from mds.core.models.encounter import Encounter
from mds.core.models.location import Location
from mds.core.models.observer import Observer
from mds.core.models.subject import Subject


__all__ = ["ANM","Patient"]

class ANM(Observer):
    
    class Meta:
        app_label = "core"
        verbose_name = 'ANM'
    locations = models.ManyToManyField('core.Location', blank=True)
    """Locations ANM is assigned to"""
    
class Patient(Subject):
    
    class Meta:
        app_label = "core"
        verbose_name = 'patient'
    secondary_id = models.CharField(max_length=12, blank=True)
    """AADHAR ID"""
    
    caregiver_name = models.CharField(max_length=128, blank=True)
    """Mother's name"""
    
    secondary_caregiver_name = models.CharField(max_length=128, blank=True)
    """Father's name"""
    
    extra_data = models.TextField(blank=True)
    """Raw data to be stored with patient.""" 
    
    def save(self, *args, **kwargs):
        tz = timezone.utc
        adj = self.dob.replace(hour=12,minute=0,second=0,microsecond=0,tzinfo=tz)
        self.dob = adj
        super(Subject, self).save(*args, **kwargs)
