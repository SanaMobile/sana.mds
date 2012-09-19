"""
Created on Feb 29, 2012

:Authors: Sana dev team
:Version: 2.0
"""
import cjson
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from sana.api import ERROR, NOTSET, LOG_LEVELS, LEVEL_CHOICES
from sana.api.models import RESTModel

# TODO read this from the config
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"

_app = "core"
class Event(RESTModel):
    """
    Logging facility for requests.
    """
    class Meta:
        app_label = _app
        
    include_link = ('uuid', 'name','level')
    include_full = ('uuid', 'name', 'level','client', 'path', 'level','message', 'timestamp', 'duration')
    include_default = include_full
    
    # max keylength of index is 767
    client = models.CharField(max_length=16)
    """ Client which made the request. """
    
    path = models.CharField(max_length=64)
    """ """
    
    level = models.IntegerField(choices=LEVEL_CHOICES, default=NOTSET)
    """ The max level of messages attached to this log. """
    
    name = models.CharField(max_length=767)
    """ The view name, or path,  of the logged target. """
    
    messages = models.TextField()
    """ JSON encoded message list """
    
    duration = models.FloatField()
    
    def settimestamp(self, value):
        self.created = value
    
    def gettimestamp(self):
        return self.created
            
    timestamp = property(fset=settimestamp, fget=gettimestamp)
    
    def getmessage(self):
        try:
            return cjson.decode(self.messages)
        except:
            return self.messages
        
    def setmessage(self, value):
        self.level = cjson.encode(value, True)
        
    message = property(fget=getmessage, fset=setmessage)
        
    def __unicode__(self):
        """ Default output """
        return _("%6s%12s%12s%s" % (self.level, self.device, self.domain, 
                    self.timestamp.strftime(settings.TIME_FORMAT)))


