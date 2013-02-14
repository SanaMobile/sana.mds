""" A set of instructions for data collection or information dissemination.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models

from ...api.utils import make_uuid

class Procedure(models.Model):
    """ A series of steps used to collect data observations. """

    uuid = models.SlugField(max_length=36, unique=True, default=make_uuid, editable=False)
    """ A universally unique identifier """
    
    created = models.DateTimeField(auto_now_add=True)
    """ When the object was created """
    
    modified = models.DateTimeField(auto_now=True)
    """ updated on modification """
   
    author = models.CharField(max_length=255)
    """ The author of the procedure """
    
    version = models.CharField(max_length=255, default="1.0")
    """ The version string for this instance """
    
    concept = models.ForeignKey('Concept', to_field='uuid')
    """ Context term for the object.""" 
    
    src = models.FileField(upload_to='core/procedure', blank=True)
    """ File storage location for the procedure """

    @property
    def name(self):
        return self.concept.display_name
    """ The title of the procedure """

    def __unicode__(self):
        return "%s %s" % (self.name,self.version)

