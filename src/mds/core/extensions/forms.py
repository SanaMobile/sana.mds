'''SSI pilot specific forms

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
           'SurgicalSubjectForm',
           'SurgicalAdvocateFollowUpForm',
           'SurgicalPatientRegistrationForm',
           'SurgicalIntakeForm'  
           ]


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
            'dob': DateSelectorInput()
        }
'''
        def clean(self):
            cleaned_data = super(SurgicalSubjectForm, self).clean()
            logging.info('clean(self)')
            use_age = self.cleaned_data.get('use_age',False)
            if use_age:
                age = int(cleaned_data.get('age',0))
                td = datetime.timedelta(years=age)
                currentYear = datetime.now().year
                first_of = datetime(datetime.now().year,1,1)
                cleaned_data['dob'] = datetime - td
            del cleaned_data['use_age']
            del cleaned_data['age']
            return cleaned_data
'''
def location_choices():
    locations = Location.objects.all()
    return (( "%s" %  location.uuid, location) for location in locations)

class SurgicalPatientRegistrationForm(forms.Form):
    # Demographics
    system_id = forms.IntegerField(label="HAS Number")
    given_name = forms.CharField(max_length=64, label='First Name')    
    family_name = forms.CharField(max_length=64, label='Name')
    dob = forms.DateField(
            widget=DateSelectorInput())
    use_age = forms.BooleanField()
    age = forms.IntegerField(required=False,
        widget=AgeInput())
    gender = forms.ChoiceField(choices=(("M","M"),("F","F")))
    image = forms.ImageField(required=False)

    location = forms.ChoiceField(choices=location_choices())
    house_number = forms.IntegerField(required=False)
    family_number = forms.IntegerField(required=False)
    telephone_number_one = forms.IntegerField(required=False) 
    telephone_number_two = forms.IntegerField(required=False) 
    telephone_number_three = forms.IntegerField(required=False) 
    telephone_number_four = forms.IntegerField(required=False)

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
    return ((unicode(x), x.uuid ) for x in Observer.objects.all())

class SurgicalIntakeForm(forms.Form):
    """ A initial encounter form
    """
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

class SurgicalAdvocateFollowUpForm(forms.Form):
    """ Visits assigned to surgical advocate post S/P
    """
    procedure = forms.ChoiceField(((x.uuid,x.title) for x in Procedure.objects.exclude(uuid__iexact="303a113c-6345-413f-88cb-aa6c4be3a07d")))
    assigned_to_sa = forms.ModelChoiceField(queryset=SurgicalAdvocate.objects.all())
    date_of_first_sa_follow_up = forms.DateTimeField(
            widget=DateSelectorInput())
    date_of_second_sa_follow_up = forms.DateTimeField(
            widget=DateSelectorInput())
    date_of_final_sa_follow_up = forms.DateTimeField(
            widget=DateSelectorInput())

class EncounterReviewForm(forms.ModelForm):
    pass

