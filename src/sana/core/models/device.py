""" An entity that  acts as a tool for data collection.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models
from sana.api.models import RESTModel
_app = "core"

class Device(RESTModel):
    """ The entity which is used to collect the data """
    class Meta:
        app_label = _app
    
    include_link = ('uuid', 'uri','name')
    include_default = include_link
    include_full = include_link
           
    name = models.CharField(max_length=36)
    """ A display name """

