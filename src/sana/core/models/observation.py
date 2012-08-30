""" An instance of data collection corresponding to a single step within a 
Procedure.

:Authors: Sana dev team
:Version: 2.0
"""
import mimetypes, os

from django.db import models
from sana.api.models import RESTModel
_app = "core"

class Observation(RESTModel):
    """ A piece of data collected about a subject during an external_id"""
    
    class Meta:
        app_label = _app    
        unique_together = (('encounter', 'node'),)

    def __unicode__(self):
        return "Observation %s %s %s %s" % (self.encounter.uuid, 
                                               self.node,
                                               self.concept.name,
                                               self.value, )
    
    include_link = ('uuid', 'uri','concept')
    include_full = ('uuid', 'uri','concept', 'encounter', 'node', 'value')
    include_default = include_link
    
    encounter = models.ForeignKey('Encounter', to_field='uuid')
    """ The instance of a procedure which this observation is associated with. """
    
    node = models.CharField(max_length=255)
    '''Unique node id within the external_id as defined by the original procedure.'''

    concept = models.ForeignKey('Concept', to_field='uuid')
    """ A dictionary entry which defines the type of information stored.""" 
    
    _value_text = models.CharField(max_length=255)
    """ A textual representation of the observation data.  For observations
        which collect file data this will be the value of the absolute
        url to the file
    """
    
    _value_complex = models.FileField(upload_to='%(app_label)/observation', blank=True,)
    """ File object holder """
    
    def getvalue(self):
        if self.is_complex():
            return self._value_complex.path
        else:
            return self._value_text
        
    def setvalue(self,value):
        if self.is_complex():
            return self._value_complex
        else:
            return self._value_text
            
    value = property(fset=setvalue,fget=getvalue)
    """ A textual representation of the observation data.  For observations
        which collect file data this will be the value of the absolute
        url to the file
    """
    
    # next two are necessary purely for packetizing
    _complex_size = models.IntegerField(default=0)
    """ Size of complex data in bytes """
    
    _complex_progress = models.IntegerField(default=0)
    """ Bytes recieved for value_complex when packetized """
    
    # Whether the binary resource was uploaded to a remote queueing
    # server.
    #uploaded = models.BooleanField(default=False)
    
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
    
    def open(self, mode="w"):
        if not self.is_complex():
            raise Exception("Attempt to open file for non complex observation")
        path, _ = os.path.split(self._value_complex.path)
        # make sure we have the directory structure
        if not os.path.exists(path):
            self.create_file()
        return open(self._value_complex.path, mode)
    
    def _generate_filename(self):
        name = '%s-%s' % (self.encounter.uuid, self.node)
        ext = mimetypes.guess(self.concept.data_type, False)
        fname = '%s%s' % (name, ext)
        
        
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
        self.value_complex = self._value_complex.field.generate_filename(self, fname)
        path, _ = os.path.split(self._value_complex.path)
        # make sure we have the directory structure
        if not os.path.exists(path):
            os.makedirs(path)
            # create the stub and commit if no exceptions
            open(self._value_complex.path, "w").close()
        self.save()
    
    def complete(self):
        if self._complex_size is 0:
            return True
        else:
            return not self._complex_progress < self._complex_size