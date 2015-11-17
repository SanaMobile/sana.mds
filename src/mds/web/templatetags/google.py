from django import template
from django.conf import settings

register = template.Library()

# settings value
@register.simple_tag
def GOOGLE_API_KEY():
    return getattr(settings, "GOOGLE_API_KEY", "")


@register.simple_tag
def GOOGLE_MAP_LAT():
    return getattr(settings, "GOOGLE_MAP_LAT", 0.0)
@register.simple_tag
def GOOGLE_MAP_LNG():
    return getattr(settings, "GOOGLE_MAP_LNG", 0.0)