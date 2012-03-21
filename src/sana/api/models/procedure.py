"""
The subject model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.db import models
from sana.api.utils import make_uuid

class Procedure(models.Model):
    """ A series of steps used to collect data observations. """
    
    uuid = models.CharField(max_length=36, unique=True, default=make_uuid,)
    """ A universally unique identifier """
    
    title = models.CharField(max_length=255)
    """ The title of the procedure """
    
    author = models.CharField(max_length=255)
    """ The author of the procedure """
    
    version = models.CharField(max_length=255, default="1.0")
    """ The version string for this instance """
    
    #text = models.TextField()
    #""" The instruction set text """
    #
    xml = models.FileField(upload_to='procedure', blank=True)
    """ File storage location for the procedure """
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % (self.title,)
