"""
The concept model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.conf import settings
from django.db import models

from sana.api.utils import make_uuid

class Concept(models.Model):
    """ A unit of knowledge."""
    def __unicode__(self):
        return self.name
    
    uuid = models.CharField(max_length=36, unique=True, default=make_uuid,)
    """ A universally unique identifier """
    
    name = models.CharField(max_length=255, unique=True)
    """ A short unique name."""
    
    display_name = models.CharField(max_length=255, blank=True)
    """ Optional descriptive name or text. """
    
    description = models.CharField(max_length=255, blank=True)
    
    data_type = models.CharField(max_length=255, 
                                 choices=settings.CONTENT_TYPES,
                                 default="text/plain")
    """ When used to refer to instance values, the type of data which will
        be stored. 
    """
    
    is_complex = models.BooleanField(default=False)
    """ True if this concept requires file storage when used for values """
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
