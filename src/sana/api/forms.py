'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 1.2
'''

from django import forms

from sana.api.models import *
from sana.api.models.deprecated import Notification

__all__ = ['AuthForm', 'ClientForm', 'ConceptForm', 'BinaryPacketForm', 
           'Base64PacketForm', 'EncounterForm', 'NotificationForm',
           'ObservationForm', 'PatientForm', 'ProcedureForm' ]

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.PasswordInput()


class ConceptForm(forms.ModelForm):
    """ A simple concept form 
    """
    class Meta:
        model = Concept


class DeviceForm(forms.ModelForm):
    """ A simple Client form
    """
    class Meta:
        model = Device

class PacketForm(forms.Form):
    encounter_guid = forms.CharField(max_length=512)
    element_id = forms.CharField()
    element_type = forms.CharField()
    binary_guid = forms.CharField()
    file_size = forms.IntegerField()
    byte_start = forms.IntegerField()
    byte_end = forms.IntegerField()
    done = forms.BooleanField(initial=False, required=False)


class BinaryPacketForm(PacketForm):
    byte_data = forms.FileField()
    
class Base64PacketForm(PacketForm):
    byte_data = forms.CharField()

class EncounterForm(forms.ModelForm):
    """ A simple encounter form. This adds the 'observations' field to handle
        json encoded observation data.
    """
    def __init__(self, *args, **kwargs):
        super(EncounterForm, self).__init__(*args,**kwargs)
        if kwargs.has_key('instance'):
            obs = self.initial['instance'].observation_set.all()
        self.fields['observations'] = forms.ModelMultipleChoiceField(obs)
        
    class Meta:
        model = Encounter

class NotificationForm(forms.Form):
    # TODO(XXX) Use a ModelForm? Type and destinations are the only thing that
    # differ.
    
    class Meta:
        model = Notification
        
    scheme = forms.ChoiceField(choices=((u'SMS', u'SMS'),
                                      (u'EMAIL', u'EMAIL')))
    destination = forms.CharField()

class ObservationForm(forms.ModelForm):
    """ A simple observation form """
    class Meta:
        model = Observation

class PatientForm(forms.ModelForm):
    """ A simple subject form
    """
    class Meta:
        model = Subject

class ProcedureForm(forms.ModelForm):
    """ A simple procedure form
    """
    class Meta:
        model = Procedure
        excludes = ('xml')