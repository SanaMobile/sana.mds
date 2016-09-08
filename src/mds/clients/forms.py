from django import forms

from .models import CrashReport

class CrashReportForm(forms.ModelForm):
    class Meta:
        model = CrashReport
    report = forms.FileField()
