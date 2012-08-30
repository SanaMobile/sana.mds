""" A set of instructions for data collection or information dissemination.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models

from sana.api.models import RESTModel
_app = "core"
class Procedure(RESTModel):
    """ A series of steps used to collect data observations. """
  
    class Meta:
        app_label = _app  
    
    include_default = ('uuid', 'name', 'author', 'version', 'uri')
    include_link = include_default
    include_full = include_default
    
    author = models.CharField(max_length=255)
    """ The author of the procedure """
    
    version = models.CharField(max_length=255, default="1.0")
    """ The version string for this instance """
    
    concept = models.ForeignKey('Concept', to_field='uuid')
    """ Context term for the object.""" 
    
    src = models.FileField(upload_to='%(app_label)/procedure', blank=True)
    """ File storage location for the procedure """

    @property
    def name(self):
        return self.concept.display_name
    """ The title of the procedure """

    def __unicode__(self):
        return "%s %s" % (self.name,self.version)

