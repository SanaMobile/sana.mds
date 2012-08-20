"""
The subject model for the Sana data engine.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models
from sana.api.models import RESTModel
_app = "core"
class Subject(RESTModel):
    """ The entity about whom data is collected. """

    class Meta:
        app_label = _app    
    concept = models.ForeignKey('Concept')
    """ A contextual term for the subject.""" 

#    def __unicode__(self):
#        return "%s, %s" % (self.name_group,self.name)
    
    