from django.utils import translation as _translation

from django.conf import settings
__all__ = [
    'activate',
    'get_and_activate',
    'get_available_languages',
    'get_request_language',
    'translate',
    'LANGUAGE_FIELD_KEY',
]

LANGUAGE_FIELD_KEY = 'language'

class Language(object):
    name = None
    code = None
    
    def __init__(self,code,name):
        self.name = name
        self.code = code
    
    def __unicode__(self):
        return name

def get_available_languages(languages=settings.LANGUAGES):
    #return [Language(x[0],x[1]) for x in languages]
    return [{ 'code':x[0], 'name': x[1] } for x in languages]
    
def get_request_language(request, lang="en", field_key=LANGUAGE_FIELD_KEY):
    language = request.REQUEST.get(LANGUAGE_FIELD_KEY, None)
    if not language:
        language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME,lang)
    return language
    
def activate(language):
    _translation.activate(language)
    
def get_and_activate(request, lang="en", field_key=LANGUAGE_FIELD_KEY):
    language = get_request_language(request, lang=lang, field_key=LANGUAGE_FIELD_KEY)
    activate(language)
    return language
    
def i18n(view_klazz):
    pass
    
def translate(view_func, lang="en", field_key=LANGUAGE_FIELD_KEY):
    def _wrapped_view_func(f, request, *args, **kwargs): 
        language = get_request_language(request, lang=lang, field_key=field_key)
        activate(language)
        #if request.session:
        #    requestion.session[settings.SESSION_KEY] = language
        return f(request,*args,**kwargs)
    return _wrapped_view_func


