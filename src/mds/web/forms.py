'''
:Authors: Sana Dev Team
:Version: 2.0
'''
import logging
from datetime import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from  django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from extra_views import InlineFormSet

from mds.core.models import *
from mds.core.widgets import *
from mds.tasks.models import *

__all__ = [
    "ProcedureForm",
    "EmptyEncounterForm",
    "EncounterTaskForm",
    "InitialTaskSetForm",
    "SurgicalSubjectForm",
    "IntakeForm",
    "AllowReadonly",
    "AllowReadonlyForm",
    "AllowReadonlyModelForm",
    "SpanField",
    "UserInline",
    "UserForm",
    "ObserverForm",
    "LoginForm",
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

def task_concepts():
    qs = Concept.objects.filter(id__in=[26,27,28,29])
    return qs

def task_subjects():
    qs = Subject.objects.all().exclude(voided=True)
    return qs
    
def task_procedures():
    qs = Procedure.objects.exclude(uuid__iexact="303a113c-6345-413f-88cb-aa6c4be3a07d")
    return qs
    
class EncounterTaskForm(forms.ModelForm):
    """ Visits assigned to surgical advocate post S/P
    """
    class Meta:
        model = EncounterTask
    subject = forms.ModelChoiceField(queryset=task_subjects(), 
        label=_("Patient"),
        to_field_name='uuid')
    procedure = forms.ModelChoiceField(queryset=task_procedures(),
        label = _('Procedure'),
        to_field_name='uuid')
    assigned_to = forms.ModelChoiceField(queryset=Observer.objects.all(),
        label = _('Assigned To'),
        to_field_name='uuid')
    concept = forms.ModelChoiceField(queryset=task_concepts(), 
        label=_("Type"),
        to_field_name='uuid')
    due_on = forms.DateTimeField(
        widget=DateTimeSelectorInput(format='%Y-%m-%d %H:%M'),
        label=_("Due On"))
    started = forms.DateTimeField(
        widget=DateTimeSelectorInput(format='%Y-%m-%d %H:%M'),
        required=False,
        label=_("Started"))
    completed = forms.DateTimeField(
        widget=DateTimeSelectorInput(format='%Y-%m-%d %H:%M'),
        required=False,
        label=_("Completed"))
    
class InitialTaskSetForm(forms.Form):
    subject = forms.ChoiceField(subject_choice_list(), label=_("Patient"))
    procedure = forms.ChoiceField(((x.uuid,x.title) for x in Procedure.objects.exclude(uuid__iexact="303a113c-6345-413f-88cb-aa6c4be3a07d")))
    assigned_to = forms.ModelChoiceField(queryset=SurgicalAdvocate.objects.all(),
        label=_('Assigned To'))
    concept = forms.ChoiceField(concept_choice_list(), 
        label=_("Type"))
    due_on = forms.DateTimeField(widget=DateSelectorInput(), 
        label=_("Initial Visit"))
    due_second = forms.DateTimeField(widget=DateSelectorInput(), label=_("Regular follow up"))
    due_thirty = forms.DateTimeField(widget=DateSelectorInput(), label=_("30 day follow up"))
    
class SurgicalSubjectForm(forms.ModelForm):
    """ A simple patient form
    """
    #use_age = forms.BooleanField()
    #age = forms.IntegerField(required=False,
    #    widget=AgeInput(),min_value=0)
    system_id = forms.CharField(max_length=64,
        label=_("HAS Number"))
    contact_one = forms.CharField(required=False,
        label=_("Telephone number one"))
    contact_two = forms.CharField(required=False,
        label=_("Telephone number two"))
    contact_three = forms.CharField(required=False,
        label=_("Telephone number three"))
    contact_four = forms.CharField(required=False,
        label=_("Telephone number four"))
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
            'house_number',
            'family_number',
            'contact_one',
            'contact_two',
            'contact_three',
            'contact_four',
        ]
        widgets = {
            'dob': DateTimeSelectorInput(),
            'label': _('Date of Birth'),
        }

def diagnosis_choices():
    choice_list = ( _("Inguinal Hernia"),
                    _("Other Hernia"),
                    _("Breat Mass"), 
                    _("Other Mass"), 
                    _("Other"))
    return ((x,x) for x in choice_list )

def operation_choices():
    choice_list = ( 
        _("Inguinal Hernia Repair"),
        _("Other Hernia Repair"),
        _("Breat Biopsy"),
        _("Mastectomy"),
        _("Mastectomy+Axillary LN Dissection"),
        _("Mastectomy+Axillary LN Biospy"),
        _("Biopsy, other"),
        _("Excision of Mass other than breast"),
        _("Other Operation"),
    )
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

class SpanField(forms.Field):
    '''A field which renders a value wrapped in a <span> tag.
    
    Requires use of specific form support. (see ReadonlyForm 
    or ReadonlyModelForm)
    '''
    
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = kwargs.get('widget', SpanWidget)
        super(SpanField, self).__init__(*args, **kwargs)

class AllowReadonly(object):
    '''Base class for ReadonlyForm and ReadonlyModelForm which provides
    the meat of the features described in the docstings for those classes.
    '''

    class NewMeta:
        readonly = tuple()

    def __init__(self, *args, **kwargs):
        super(AllowReadonly, self).__init__(*args, **kwargs)
        readonly = self.NewMeta.readonly
        if not readonly:
            return
        for name, field in self.fields.items():
            if name in readonly:
                field.widget = SpanWidget()
            elif not isinstance(field, SpanField):
                continue
            field.widget.original_value = str(getattr(self.instance, name))

class AllowReadonlyForm(AllowReadonly, forms.Form):
    '''A form which provides the ability to specify certain fields as
    readonly, meaning that they will display their value as text wrapped
    with a <span> tag. The user is unable to edit them, and they are
    protected from POST data insertion attacks.
    
    The recommended usage is to place a NewMeta inner class on the
    form, with a readonly attribute which is a list or tuple of fields,
    similar to the fields and exclude attributes on the Meta inner class.
    
        class MyForm(ReadonlyForm):
            foo = forms.TextField()
            class NewMeta:
                readonly = ('foo',)
    '''
    pass

class AllowReadonlyModelForm(AllowReadonly, forms.ModelForm):
    '''A ModelForm which provides the ability to specify certain fields as
    readonly, meaning that they will display their value as text wrapped
    with a <span> tag. The user is unable to edit them, and they are
    protected from POST data insertion attacks.
    
    The recommended usage is to place a NewMeta inner class on the
    form, with a readonly attribute which is a list or tuple of fields,
    similar to the fields and exclude attributes on the Meta inner class.
    
        class Foo(models.Model):
            bar = models.CharField(max_length=24)

        class MyForm(ReadonlyModelForm):
            class Meta:
                model = Foo
            class NewMeta:
                readonly = ('bar',)
    '''
    pass

class ProcedureForm(AllowReadonlyModelForm):
    class Meta:
        model = Procedure
    class NewMeta:
        readonly = ['uuid','created',]

class UserInline(InlineFormSet):
    model = User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password', "first_name", 'last_name',)
        widgets = (
            {'password': forms.PasswordInput(attrs={
                "autocomplete":"off",
                "type":'password'}) },
            {'username': forms.TextInput(attrs={"autocomplete":"off"}) },
        )
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
        widgets = { 
            'password': PasswordInput(),
        }

class BlankUserForm(UserForm):

    def __init__(self,**kwargs):
        if kwargs.get('instance',None):
            kwargs['instance'] = None
        if kwargs.get('data',None):
            kwargs['data'] = None
            kwargs['data'] = None
        UserForm.__init__(self, **kwargs)

class ObserverForm(forms.ModelForm):
    class Meta:
        model =User
