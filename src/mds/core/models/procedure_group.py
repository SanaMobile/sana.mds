""" A group of procedures. Note there is a many-to-many relationship between procedure and procedure groups

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mds.api.utils import make_uuid
@python_2_unicode_compatible
class ProcedureGroup(models.Model):
    """ A group of procedures"""

    class Meta:
        app_label = "core"
    uuid = models.SlugField(max_length=36, unique=True, default=make_uuid, editable=False)
    """ A universally unique identifier """
    
    created = models.DateTimeField(auto_now_add=True)
    """ When the object was created """
    
    modified = models.DateTimeField(auto_now=True)
    """ updated on modification """
   
    title = models.CharField(max_length=255)
    """ A descriptive title for the procedure group. """
   
    author = models.CharField(max_length=255)
    """ The creator of the procedure group """
    
    description = models.TextField()
    """ Additional narrative information about the group of procedures. """
    
    procedures = models.ManyToManyField('Procedure', related_name='groups')

    voided = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.title)

