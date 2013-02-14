""" An entity about whom data is collected.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models
from ...api.utils import make_uuid

class AbstractSubject(models.Model):
    """ The entity about whom data is collected. """
    class Meta:
        abstract = True
    
    uuid = models.SlugField(max_length=36, unique=True, default=make_uuid, editable=False)
    """ A universally unique identifier """
    
    created = models.DateTimeField(auto_now_add=True)
    """ When the object was created """
    
    modified = models.DateTimeField(auto_now=True)
    """ updated on modification """
    
class Subject(AbstractSubject): 
    """ Simple subject implementation as a medical patient. 
    """
    class Meta:
        app_label = "core"
    given_name = models.CharField(max_length=64)
    
    family_name = models.CharField(max_length=64)
    
    dob = models.DateField()
    
    @property
    def age(self):
        #TODO Have this return calculated current age - dob
        pass
    
    gender = models.CharField(choices=(("M","M"),("F","F")),max_length=2)
    
    