from django.forms import widgets

def hide_if_initialized(form, field):
    if field:
        widget = forms.HiddenInput()
    else:
        widget = field.widget
    return widget