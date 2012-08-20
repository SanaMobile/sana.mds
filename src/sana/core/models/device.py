"""
The device model for the Sana data engine.

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
        
    name = models.CharField(max_length=36)
    """ A display name """

