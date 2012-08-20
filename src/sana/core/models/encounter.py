"""
The encounter model for the Sana data engine.

:Authors: Sana dev team
:Version: 2.0
"""

from django.db import models
from sana.api.models import RESTModel

_app="core"

class Encounter(RESTModel):
    """ A completed procedure, where data has been collected
    """
    class Meta:
        app_label = _app
               
    def __unicode__(self):
        return "Encounter %s %s" % (self.uuid, self.created)

    
#    # Will need this for date of collection as well - separate from created which 
#    # marks when brought into existence on the server(needed for QC)
#    date = models.DateTimeField()
#    """ The date and time the encounter was completed upon the subject. """
    
    procedure = models.ForeignKey('Procedure')
    """ The procedure used to collect this encounter """
    
    observer = models.ForeignKey('Observer')
    """ The entity which collected the data """
    
    device = models.ForeignKey('Device')
    """ The client which collected the encounter """
    
    subject = models.ForeignKey('Subject')
    """ The subject about whom the data was collected """

    concept = models.ForeignKey('Concept')
    """ A contextual term for the encounter."""

    #_uploaded = models.BooleanField(default=False)
    #""" Whether the saved procedure was uploaded to a remote queueing server. """
    

    # EMR Encounter Number
    # Might be cleaner to make this an integer, but EMR systems in general
    # might not use an integer as the unique ID of an external_id.
    #external_id = models.CharField(default="-1", max_length=512)
    
    #TODO move these to a manager class
    def flush(self):
        """ Removes the responses text and files for this Encounter """
        self.save()
        for obs in self.observation_set.all():
                obs.flush();
                
    def complete(self):
        complete = True
        for obs in self.observation_set.all():
            complete = complete and obs.complete()
            if not complete:
                break
        return complete
