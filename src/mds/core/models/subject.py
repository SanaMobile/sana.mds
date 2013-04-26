""" An entity about whom data is collected.

:Authors: Sana dev team
:Version: 2.0
"""
import datetime
from django.db import models
from mds.api.utils import make_uuid

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
    
    dob = models.DateTimeField()
    
    gender = models.CharField(choices=(("M","M"),("F","F")),max_length=2)
    
    image = models.ImageField(blank=True, upload_to="core/subject")
    
    location = models.ForeignKey('Location', blank=True, to_field='uuid')
    
    @property
    def age(self):
        """ Convenience wrapper to calculate the age. """
        today = datetime.date.today()
        if self.dob > datetime.date.today().replace(year=self.dob.year):
            return today.year -self.dob.year - 1
        else:
            return today.year -self.dob.year

    