"""
The observation model for the Sana data engine.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models

from django.contrib.auth.models import User
from sana.api.models import RESTModel

_app = "core"
class Observer(RESTModel):
    """ The user who executes the Procedure and collects the Observations """
        
    class Meta:
        app_label = _app
    user = models.OneToOneField(User, unique=True)
    """ A universally unique identifier. See  """

    
