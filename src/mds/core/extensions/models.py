"""
Extensions for core models

:Authors: Sana dev team
:Version: 2.0
"""
from django.db import models

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


