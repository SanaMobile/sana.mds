from django import forms

from mds.core.widgets import *
from .models import *

__all__ = [ 'EncounterTaskForm',
            'ObservationTaskForm']

class EncounterTaskForm(forms.ModelForm):
    class Meta:
        model = EncounterTask
        widgets = {
            'due_on': DateTimeSelectorInput(),
            'started': DateTimeSelectorInput(),
            'completed': DateTimeSelectorInput(),

        }
class ObservationTaskForm(forms.ModelForm):
    class Meta:
        model = ObservationTask
