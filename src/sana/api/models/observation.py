"""
The observation model for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""
import mimetypes, os

from django.db import models


class Observation(models.Model):
    """ A piece of data collected about a subject during an external_id"""
    
    class Meta:
        unique_together = (('encounter', 'node'),)

    def __unicode__(self):
        return "Observation %s %s %s %s" % (self.encounter.uuid, 
                                               self.node,
                                               self.concept.name,
                                               self.value, )

    encounter = models.ForeignKey('Encounter')
    """ The instance of a procedure which this observation is associated with. """
    
    node = models.CharField(max_length=255)
    '''Unique node id within the external_id as defined by the original procedure.'''

    concept = models.ForeignKey('Concept')
    """ A dictionary entry which defines the type of information stored.""" 
    
    value = models.CharField(max_length=255)
    """ A textual representation of the observation data.  """
    
    value_complex = models.FileField(upload_to='observation', blank=True,)
    """ A a resource identifier for the data"""
    
    # next two are necessary purely for packetizing
    _complex_size = models.IntegerField(default=0)
    """ Size of complex data in bytes """
    
    _complex_progress = models.IntegerField(default=0)
    """ Bytes recieved for value_complex when packetized """
    
    # Whether the binary resource was uploaded to a remote queueing
    # server.
    uploaded = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    @property
    def subject(self):
        """ Convenience wrapper around Encounter.subject """
        if self.encounter:
            subj = self.encounter.subject
        else:
            subj = None
        return subj
    
    @property
    def is_complex(self):
        """ Convenience wrapper around Concept.is_complex """
        if self.concept:
            return self.concept.is_complex
        else:
            False
    
    @property
    def data_type(self):
        """ Convenience wrapper around Concept.data_type """
        if self.concept:
            return self.concept.data_type
        else:
            return None
            
    def create_file(self, append=None):
        """ Creates a zero length file stub on disk
            Parameters:
            append
                Extra string to append to file name.
        """
        name = '%s-%s' % (self.encounter.uuid, self.node)
        if append:
            name += '-%s' % append
        ext = mimetypes.guess(self.concept.data_type, False)
        fname = '%s%s' % (name, ext)
        self.value_complex = self.value_complex.field.generate_filename(self, fname)
        path, _ = os.path.split(self.value_complex.path)
        # make sure we have the directory structure
        if not os.path.exists(path):
            os.makedirs(path)
        # create the stub and commit if no exceptions
        open(self.value_complex.path, "w").close()
        self.save()
    
    def complete(self):
        if self._complex_size is 0:
            return True
        else:
            return not self._complex_progress < self._complex_size 