"""
The subject model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.db import models
from sana.api.utils import make_uuid

class Subject(models.Model):
    """ The entity about whom data is collected. """
        
    uuid = models.CharField(max_length=36, unique=True, 
                            default=make_uuid,)
        
    name = models.CharField(max_length=512)
    """ A given or singular name """
    
    name_group = models.CharField(max_length=512)
    """ A group name such as family """
    
    latitude = models.FloatField()
    """ The GPS latitude coordinate. """
 
    longitude = models.FloatField()
    """ The GPS longitude coordinate. """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s, %s" % (self.name_group,self.name)