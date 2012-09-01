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
           'EventForm',
           'NotificationForm',
           'ObserverForm', 
           'ObservationForm', 
           'SubjectForm', 
           'ProcedureForm',
           'SessionForm'  ]

class SessionForm(forms.Form):
    """ Authentication Form """
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
    """ A simple encounter form.
    """
    class Meta:
        model = Encounter

class EventForm(forms.ModelForm):
    """ A simple event form
    """
    class Meta:
        model = RequestLog

class NotificationForm(forms.ModelForm):
    """ Form for sending notifications """
    class Meta:
        model = Notification

class ObservationForm(forms.ModelForm):
    """ A simple observation form """
    class Meta:
        model = Observation
        fields = ('encounter', 'concept', 'node', '_value_complex')

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

