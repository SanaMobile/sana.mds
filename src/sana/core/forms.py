'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''

from django import forms

from sana.core.models import *

__all__ = ['ConceptForm', 'RelationshipForm', 'RelationshipCategoryForm', 
           'DeviceForm',
           'EncounterForm', 
           'NotificationForm',
           'ObserverForm', 
           'ObservationForm', 
           'SubjectForm', 
           'ProcedureForm',  ]

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.PasswordInput()

class ConceptForm(forms.ModelForm):
    """ A simple concept form 
    """
    class Meta:
        model = Concept

class RelationshipForm(forms.ModelForm):
    """ A simple concept relationship form 
    """
    class Meta:
        model = Relationship

class RelationshipCategoryForm(forms.ModelForm):
    """ A simple concept relationship category form 
    """
    class Meta:
        model = RelationshipCategory

class DeviceForm(forms.ModelForm):
    """ A simple Client form
    """
    class Meta:
        model = Device

class EncounterForm(forms.ModelForm):
    """ A simple encounter form. This adds the 'observations' field to handle
        json encoded observation data.
    """
    def __init__(self, *args, **kwargs):
        super(EncounterForm, self).__init__(*args,**kwargs)
        if kwargs.has_key('instance'):
            obs = self.initial['instance'].observation_set.all()
        self.fields['observations'] = forms.ModelMultipleChoiceField(obs,required=False)
        
    class Meta:
        model = Encounter

class EventForm(forms.ModelForm):
    """ A simple event form
    """
    class Meta:
        model = RequestLog

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

class ObserverForm(forms.ModelForm):
    """ A simple observation form """
    class Meta:
        model = Observer

class ProcedureForm(forms.ModelForm):
    """ A simple procedure form
    """
    class Meta:
        model = Procedure

class RequestLogForm(forms.ModelForm):
    """ A simple request log form
    """
    class Meta:
        model = RequestLog
     
class SubjectForm(forms.ModelForm):
    """ A simple subject form
    """
    class Meta:
        model = Subject

# Extra form bits
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