""" Handler extensions
"""
from mds.api.handlers import DispatchingHandler
from mds.api.decorators import logged

from .forms import ANMForm, PatientForm
from .models import ANM, Patient

@logged
class ANMHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = ANM
    form = ANMForm
    fields = (
        "uuid",
        ("user",("username","is_superuser")),
        ("locations",("uuid", "name")),
        "modified",
        "created",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class PatientHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = Patient
    form = PatientForm
    fields = (
        "uuid",
        "family_name",
        "given_name",
        "gender",
        "dob",
        "image",
        "system_id",
        "secondary_id",
        "caregiver_name",
        "secondary_caregiver_name"
        ("location",("name","uuid")),
        "modified",
        "created",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
