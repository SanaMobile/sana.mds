import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from extra_views import ModelFormSetView

from mds.core.widgets import *
from mds.core.models import *
from mds.tasks.models import *
#from .models import *

__all__ = [ 'SimpleEncounterTaskSetForm',
            'SurgicalAdvocateFollowUpForm']
            
class SimpleEncounterTaskSetForm(forms.ModelForm):
    """ Visits assigned to surgical advocate post S/P
    """
    class Meta:
        model = EncounterTask
        fields = [
            'subject',
            'procedure',
            'assigned_to',
            'assigned_to',
            'due_on',
        ]
        widgets = {
            'due_on' : forms.DateTimeField(
                            widget=DateTimeSelectorInput(format='%Y-%m-%d %H:%M'),
                            label=_("Due On")),
        }


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

class QueryForm(forms.Form):

    def qfilter(self):
        squery = {}
        if self.is_valid():
            for k,v in self.cleaned_data.items():
                if v:
                    squery[k] = v
        return squery

class EncounterQueryForm(forms.Form):
    observer = forms.ModelChoiceField(queryset=SurgicalAdvocate.objects.all())
    start_date = forms.DateTimeField(
            label=_('After'),
            widget=DateSelectorInput())
    end_date = forms.DateTimeField(
            label=('Before'),
            widget=DateSelectorInput())
    operation = forms.ChoiceField(choices=settings.ALLOWED_OPERATIONS)
    gender = forms.ChoiceField(label=_('Gender'), choices=settings.GENDER_CHOICES)
    min_age = forms.IntegerField(label=_('Min age'), min_value=0)
    max_age = forms.IntegerField(label=_('Max age'), max_value=120)
    given_name = forms.CharField(label=_('Given Name'))
    family_name = forms.CharField(label=_('Family Name'))

    def qfilter(self):
        datefmt = '%Y-%m-%d'
        squery = {}
        if self.is_valid():
            data = self.cleaned_data
            # Subject query filters
            system_id = data.get('system_id',None)
            if system_id:
                squery['subject__system_id__exact'] = system_id
            if given_name:
                squery["subject__given_name__contains"] = given_name
            family_name = data.get('family_name',None)
            if family_name:
                squery["subject__family_name__contains"] = family_name
            gender = data.get('gender',None)
            if gender:
                squery["subject__gender__exact"] = gender
            
            now = datetime.datetime.now()
            min_age = data.get('min_age', None)
            if min_age:
                squery["subject__dob__gte"] = min_age
            max_age = data.get('max_age', None)
            if max_age:
                squery["subject__dob__lte"] = given_name
                
            # get start and end date strings
            start_str = data.get('start', None)
            end_str = data.get('end', None)
    
            # set the end datetime
            if end_str:
                end_date = datetime.datetime.strptime(end_str[:10],datefmt)
            else:
                end_date = now.replace(day=1) - datetime.timedelta(days=1)
                
            # set the start datetime
            if start_str:
                start_date = datetime.datetime.strptime(start_str[:10],datefmt )
            elif end_str:
                start_date = end_date - datetime.timedelta(days=30)
            else:
                start_date = end_date.replace(day=1)
            squery['created__range']=[start_date, end_date]
        return squery

class SubjectQuery(QueryForm):
    gender = forms.ChoiceField(label=_('Gender'), choices=settings.GENDER_CHOICES)
    min_age = forms.IntegerField(label=_('Min age'), min_value=0, max_value=120)
    max_age = forms.IntegerField(label=_('Max age'), min_value=0, max_value=120)
    given_name = forms.CharField(label=_('Given Name'))
    family_name = forms.CharField(label=_('Family Name'))
