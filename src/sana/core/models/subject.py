""" An entity about whom data is collected.

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
    
    include_link = ('uuid', 'uri','concept')
    include_full = include_link
    include_default = include_link
    
    concept = models.ForeignKey('Concept', to_field='uuid')
    """ A contextual term for the subject.""" 

    
    