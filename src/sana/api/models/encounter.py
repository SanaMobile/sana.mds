"""
The encounter model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""

from django.conf import settings
from django.db import models
from sana.api.utils import make_uuid

class Encounter(models.Model):
    """ An external_id, representing a completed procedure, where data has been
        collected
    """
    class Meta:
        app_label = 'mrs'
        
    def __init__(self,*pargs,**kwargs):
        models.Model.__init__(self, *pargs, **kwargs)
        
    def __unicode__(self):
        return "Encounter %s %s" % (self.uuid, self.created)

    uuid = models.CharField(max_length=36, unique=True, default=make_uuid,)
    """ A universally unique identifier """
    
#    # Will need this for date of collection as well - separate from created which 
#    # marks when brought into existence on the server(needed for QC)
#    date = models.DateTimeField()
#    """ The date and time the encounter was completed upon the subject. """
    
    procedure = models.ForeignKey('Procedure')
    """ The procedure used to collect this encounter """
    
    worker = models.ForeignKey('Worker')
    """ The entity which collected the data """
    
    device = models.ForeignKey('Device')
    """ The client which collected the encounter """
    
    subject = models.ForeignKey('Subject')
    """ The subject about whom the data was collected """
    
    # Text responses of the saved procedure
    #responses = models.TextField()

    # OpenMRS login credentials for this user
    #upload_username = models.CharField(max_length=512)
    #upload_password = models.CharField(max_length=512)
    #observations = models.ManyToManyField(Observation)

    uploaded = models.BooleanField(default=False)
    """ Whether the saved procedure was uploaded to a remote queueing server. """
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # EMR Encounter Number
    # Might be cleaner to make this an integer, but EMR systems in general
    # might not use an integer as the unique ID of an external_id.
    #external_id = models.CharField(default="-1", max_length=512)
    
    def flush(self):
        """ Removes the responses text and files for this Encounter """
        self.save()
        if settings.FLUSH_BINARYRESOURCE:
            for obs in self.observation_set.all():
                obs.flush();
    def complete(self):
        complete = True
        for obs in self.observation_set.all():
            complete = complete and obs.complete()
            if not complete:
                break
        return complete
    