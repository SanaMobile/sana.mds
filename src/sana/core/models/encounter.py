""" An instance of data collection resulting from executing a Procedure
on a Subject.

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
    
    include_link = ('uuid', 'uri','modified','subject', 'procedure')
    include_default = include_link
    include_full = ('uuid', 'uri','modified','subject', 'procedure', 
                    'observer', 'device', 'concept')
    
    procedure = models.ForeignKey('Procedure', to_field='uuid')
    """ The procedure used to collect this encounter """
    
    observer = models.ForeignKey('Observer', to_field='uuid')
    """ The entity which collected the data """
    
    device = models.ForeignKey('Device', to_field='uuid')
    """ The client which collected the encounter """
    
    subject = models.ForeignKey('Subject', to_field='uuid')
    """ The subject about whom the data was collected """

    concept = models.ForeignKey('Concept', to_field='uuid')
    """ A contextual term for the encounter."""

    #_uploaded = models.BooleanField(default=False)
    #""" Whether the saved procedure was uploaded to a remote queueing server. """
    
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
