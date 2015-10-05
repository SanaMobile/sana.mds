from django import forms
from extra_views import ModelFormSetView

from mds.core.widgets import *
from .models import *

__all__ = [ 'EncounterTaskForm',
            'ObservationTaskForm']
            
class SharedValueSimpleEncounterTaskForm(forms.ModelForm):
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

