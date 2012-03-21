"""
The device model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.db import models
from sana.api.utils import make_uuid


## ? Makes more sense than 'Client'
class Device(models.Model):
    """ The entity which is used to collect the data """
    uuid = models.CharField(max_length=36, unique=True, default=make_uuid)
    name = models.CharField(max_length=36)

