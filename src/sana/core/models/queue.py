'''
Created on Aug 9, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.db import models
from sana.api.models import RESTModel

QUEUE_STATUS=((0,'Failed Dispatch'))
_app = "core"
class QueueElement(RESTModel):
    """ An element that is being processed
    """
    
    class Meta:
        app_label = _app
    object_url = models.CharField(max_length=512)
    """ The uuid of the cached object """
    
    @property
    def object_uuid(self):
        return ''
    
    cache = models.TextField(blank=True)
    """ Dump of the form data for the object """
    
    status = models.IntegerField(choices=QUEUE_STATUS)
    """ Current state in the queue """
    
    message = models.TextField(blank=True)
    """ Useful messages returned from processing """