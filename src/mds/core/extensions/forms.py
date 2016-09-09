'''
Project specific extensions to core forms

:Authors: Sana Dev Team
:Version: 2.0
'''

from django import forms
from .models import ANM, Patient

__all__ = [
    'ANMForm',
    'PatientForm'
    ]

class ANMForm(forms.ModelForm):
    class Meta:
        model = ANM
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
