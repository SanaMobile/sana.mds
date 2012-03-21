"""
The observation model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.db import models
from sana.api.utils import make_uuid

from django.contrib.auth.models import User

## Going to Need this at some point for QC. ?Auth?    
class Worker(models.Model):
    """ The user who executes the Procedure and collects the Observations """
    user = models.OneToOneField(User, unique=True)
    uuid = models.CharField(max_length=36, unique=True, default=make_uuid,)
    """ A universally unique identifier. See  """
    
