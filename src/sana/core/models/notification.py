"""
Notifications for the Sana data engine.

:Authors: Sana dev team
:Version: 2.0
"""
import cjson

from django.db import models
from sana.api.models import RESTModel
_app="core"
class Notification(RESTModel):
    """ A message to be sent """
    
    class Meta:
        app_label = _app
    address = models.CharField(max_length=512)
    """ The recipient address """
    
    header = models.CharField(max_length=512)
    """ Short descriptive text; i.e. subject field """

    message = models.TextField()
    """ The message body """
    
    delivered = models.BooleanField(default = False)
    """ Set True when delivered """

    def to_json(self, **kwargs):
        msg = {'address': self.client,
               'subject': self.header,
               'message': self.message,}
        for k,v in kwargs.iteritems():
            msg[k] = v
        return cjson.encode(msg)
