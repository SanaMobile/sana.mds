'''
:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
from datetime import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from mds.core.models import *
from mds.core.widgets import *

__all__ = [
    "EmptyEncounterForm",
    "EncounterTaskForm",
    "InitialTaskSetForm",
    "SurgicalSubjectForm",
    "IntakeForm",
    ]

def subject_choice_list():
    subject_list = (
        (x.uuid, u"%s - %s, %s" % (x.system_id,x.family_name, x.given_name)) for x in Subject.objects.all().exclude(voided=True))
    return  subject_list

def concept_choice_list():
    concepts = [
        Concept.objects.get(pk=28),
        Concept.objects.get(pk=27),
        Concept.objects.get(pk=26),
        Concept.objects.get(pk=29),
    ]
    return ((x.uuid, x.display_name) for x in concepts)

class EmptyEncounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        widgets = {
            "device":forms.HiddenInput(),
            "procedure":forms.HiddenInput(),
            "observer" :forms.HiddenInput(),
            "concept":forms.HiddenInput(),
        }

class EncounterTaskForm(forms.Form):
    """ Visits assigned to surgical advocate post S/P
    """
    subject = forms.ChoiceField(subject_choice_list(), label="Patient")
    procedure = forms.ChoiceField(((x.uuid,x.title) for x in Procedure.objects.exclude(uuid__iexact="303a113c-6345-413f-88cb-aa6c4be3a07d")))
    assigned_to = forms.ModelChoiceField(queryset=SurgicalAdvocate.objects.all())
    concept = forms.ChoiceField(concept_choice_list(), label="Type")
    #due_on = forms.DateTimeField(widget=DateSelectorInput())

class InitialTaskSetForm(EncounterTaskForm):
    due_on = forms.DateTimeField(widget=DateSelectorInput(), label="Initial Visit")
    due_second = forms.DateTimeField(widget=DateSelectorInput(), label="Regular follow up")
    due_thirty = forms.DateTimeField(widget=DateSelectorInput(), label="30 day follow up")
class SurgicalSubjectForm(forms.ModelForm):
    """ A simple patient form
    """
    #use_age = forms.BooleanField()
    #age = forms.IntegerField(required=False,
    #    widget=AgeInput(),min_value=0)
    system_id = forms.CharField(max_length=64,label="HAS Number")
    contact_one = forms.CharField(required=False,label="Telephone number one")
    contact_two = forms.CharField(required=False,label="Telephone number two")
    contact_three = forms.CharField(required=False,label="Telephone number three")
    contact_four = forms.CharField(required=False,label="Telephone number four")
    class Meta:
        model = SurgicalSubject
        fields = [
            'system_id',
            'family_name',
            'given_name',
            'dob',
            'gender',
            'image',
            'location',
            #'national_id',
            'house_number',
            'family_number',
            'contact_one',
            'contact_two',
            'contact_three',
            'contact_four',
        ]
        widgets = {
            'dob': DateTimeSelectorInput()
        }

def diagnosis_choices():
    choice_list = ( "Inguinal Hernia",
                    "Other Hernia",
                    "Breat Mass", 
                    "Other Mass", 
                    "Other")
    return ((x,x) for x in choice_list )

def operation_choices():
    choice_list = ( "Inguinal Hernia Repair",
                    "Other Hernia Repair",
                    "Breat Biopsy",
                    "Mastectomy",
                    "Mastectomy+Axillary LN Dissection",
                    "Mastectomy+Axillary LN Biospy",
                    "Biopsy, other",
                    "Excision of Mass other than breast",
                    "Other Operation")
    return ( (x,x) for x in choice_list)
    
def advocate_choices():
    choice_list = None
    return ((unicode(x), x.uuid ) for x in SurgicalAdvocate.objects.all())

class IntakeForm(forms.ModelForm):
    """ A initial encounter form
    """
    class Meta:
        model = Encounter
        widgets = {
            "device":forms.HiddenInput(),
            "procedure":forms.HiddenInput(),
            "observer" :forms.HiddenInput(),
            "concept":forms.HiddenInput(),
            "voided":forms.HiddenInput(),
        }

    #device = forms.SlugField(widget=forms.HiddenInput(),
    #    initial="2fc0a9f7-384b-4d97-8c1c-aa08f0e12105")
    """
    procedure = forms.CharField(widget=forms.HiddenInput(),
        initial="303a113c-6345-413f-88cb-aa6c4be3a07d")
    observer = forms.SlugField(widget=forms.HiddenInput())
    subject = forms.ChoiceField(subject_choice_list(), label="Patient")
    """
    subject = forms.ChoiceField(subject_choice_list(), label="Patient")
    # Observation data
    diagnosis = forms.ChoiceField(choices=diagnosis_choices())
    diagnosis_other = forms.CharField(required=False)
    operation = forms.MultipleChoiceField(choices=operation_choices())
    operation_other = forms.CharField(required=False)
    date_of_operation = forms.DateField(
            widget=DateSelectorInput())
    date_of_discharge = forms.DateField(
            widget=DateSelectorInput())
    date_of_regular_follow_up = forms.DateField(
            widget=DateSelectorInput())

