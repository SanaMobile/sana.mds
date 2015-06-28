''' Representation of QOS data sent from clients
'''
from django.db import models
from mds.core.models import Device

class ClientQOS(models.Model):
    """ Object representing transmission data sent from client
    """
    source = models.ForeignKey('Device', related_name='qos_events')
    target = models.CharField(max_length=255)
    sent = models.DateTimeField()
    received = models.DateTimeField()
    send_count = models.IntegerField(default=1)
    event_start = models.DateTimeField(blank=True)
    event_complete = models.DateTimeField(blank=True)
    request_complete = models.DateTimeField()
