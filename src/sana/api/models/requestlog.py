'''
Created on Feb 29, 2012

@author: nojnk
'''

from django.db import models

# TODO read this from the config
TIME_FORMAT = "%m/%d/%Y %H:%M:%S"

class RequestLog(models.Model):
    """
    Logging facility for requests.
    """
    class Meta:
        app_label = 'mrs'

    def __unicode__(self):
        return u"%s : %s : Duration: %0.4fs" % (self.uri,
                                 self.timestamp.strftime(TIME_FORMAT),
                                 self.duration)

    # max keylength of index is 767
    uri = models.CharField(max_length=767)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField()

