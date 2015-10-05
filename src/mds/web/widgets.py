from django.forms import widgets
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

__all__ = [
    "hide_if_initialized",
    "SpanWidget",
    "SelectOrTextWidget",
    "MultiSelectWithTextWidget",
    ]
    
def hide_if_initialized(form, field):
    if field:
        widget = forms.HiddenInput()
    else:
        widget = field.widget
    return widget
    

class SpanWidget(forms.Widget):
    '''Renders a value wrapped in a <span> tag.
    
    Requires use of specific form support. (see ReadonlyForm 
    or ReadonlyModelForm)
    '''

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<span%s >%s</span>' % (
            forms.util.flatatt(final_attrs), self.original_value))

    def value_from_datadict(self, data, files, name):
        return self.original_value

class ModelSelectOrNewWidget(forms.Select):

    def render(self, name, value, attrs=None):
        _url = None
        output = []
        output.append(super(ModelSelectOrNewWidget,self).render(name,value,attrs))
        output.append("<a href='%s'><img src='/mds/static/admin/img/icon_addlink.gif'/></a>" % _url)
        return mark_safe(u''.join(output))

class SingleOrMultiWidget(forms.MultiWidget):

    checkbox_label  = _('Show all')

    def __init__(self, widgets, attrs=None):
        self.widgets = [widgets.CheckBoxInput(attrs)]
        for widget in [w() if isinstance(w, type) else w for w in widgets]:
            self.widgets.append(widget)
        super(SingleOrMultiWidget, self).__init__(attrs)
    
    def decompress(self,value):
        if value:
            value = value.split(',')
        
    def render(self, name, value, attrs=None):
        output = []
        output.append(widgets)
        output.append(super(MultiValueToggleMixin, self).render(name,value,attrs))
        return mark_safe(u''.join(output))




class SelectOrTextWidget(forms.MultiWidget):
    other = None

    def __init__(self, attrs=None, choices=None, other=None):
        widgets = (
            forms.Select(attrs=attrs, choices=choices),
            forms.TextInput(attrs=attrs),
        )
        super(SelectOrTextWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            data = value.split(',')
            return [data[0], data[1]]
        return [None, None]

    def format_output(self, rendered_widgets):
        
        return u'\n'.join(rendered_widgets)

class MultiSelectWithTextWidget(forms.MultiWidget):
    other = None

    def __init__(self, attrs=None, choices=None, other=None):
        widgets = (
            forms.SelectMultiple(attrs=attrs, choices=choices),
            forms.TextInput(attrs=attrs),
        )
        super(MultiSelectWithTextWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            data = value.split(',')
            return data
        return []

    def format_output(self, rendered_widgets):
        
        return u'\n'.join(rendered_widgets)
